from typing import Optional

from genx_ai_camera_panel.constants import TUNNEL_HOST
from genx_ai_camera_panel.db import DB, RemotePortMappingTableIndex
from genx_ai_camera_panel.tunnel_helper import TunnelHelper
from onvif.onvif_client import OnvifClient, WsDiscoveryClient


class OnvifWrapper:
    db: DB
    tunnel_helper: TunnelHelper

    def __init__(self) -> None:
        self.db = DB()
        self.tunnel_helper = TunnelHelper()

    def scan(
        self,
        username: Optional[str],
        password: Optional[str],
    ):
        """
        Scan for available ONVIF devices.

        Returns:
            A list of dictionaries, each containing the device's IP address,
            port, and protocol (TCP or UDP).
        """

        wsd_client = WsDiscoveryClient()
        nvts = wsd_client.search()

        for nvt in nvts:
            self.scan_device(
                nvt.ip_address,
                nvt.port,
                username,
                password,
            )

        wsd_client.dispose()

    def scan_device(
        self,
        ip_address: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
    ):
        """
        Scan a single ONVIF device.
        """
        try:
            print(f"[*] Scanning device: {ip_address}:{port}")
            onvif_client = OnvifClient(ip_address, port, username, password)

            hostname = onvif_client.get_hostname() or {}
            device_information = onvif_client.get_device_information()
            if device_information is None:
                return

            manufacturer, model, firmware_version, serial_number, hardware_id = (
                self._extract_device_info(device_information)
            )
            profile_tokens = onvif_client.get_profile_tokens()
            video_configurations = onvif_client.get_video_encoder_configurations()

            for index, profile_token in enumerate(profile_tokens):
                profile_data = {
                    "index": index,
                    "profile_token": profile_token,
                    "ip_address": ip_address,
                    "port": port,
                    "username": username,
                    "password": password,
                    "manufacturer": manufacturer,
                    "model": model,
                    "firmware_version": firmware_version,
                    "serial_number": serial_number,
                    "hardware_id": hardware_id,
                }

                self._process_profile(
                    profile_data,
                    video_configurations,
                    onvif_client,
                    hostname,
                )
        except Exception as exception:
            print(exception)

    def _extract_device_info(self, device_information):
        manufacturer = device_information["Manufacturer"] or ""
        model = device_information["Model"] or ""
        firmware_version = device_information["FirmwareVersion"] or ""
        serial_number = device_information["SerialNumber"] or ""
        hardware_id = device_information["HardwareId"] or ""

        return manufacturer, model, firmware_version, serial_number, hardware_id

    def _process_profile(
        self,
        profile_data: dict,
        video_configurations: list,
        onvif_client,
        hostname: dict,
    ):
        index = profile_data["index"]
        profile_token = profile_data["profile_token"]
        ip_address = profile_data["ip_address"]
        port = profile_data["port"]
        username = profile_data["username"]
        password = profile_data["password"]
        manufacturer = profile_data["manufacturer"]
        model = profile_data["model"]
        firmware_version = profile_data["firmware_version"]
        serial_number = profile_data["serial_number"]
        hardware_id = profile_data["hardware_id"]

        stream_url = onvif_client.get_streaming_uri(profile_token)
        video_configuration = video_configurations[index]
        resolution = f"{video_configuration['Resolution']['Width']}x{video_configuration['Resolution']['Height']}"
        fps = video_configuration["RateControl"]["FrameRateLimit"]
        bitrate = video_configuration["RateControl"]["BitrateLimit"]
        encoding = video_configuration["Encoding"]

        if stream_url and ip_address and port:
            mapped_port = self.db.get_remote_port_mapping(ip_address, port)
            remote_ip = TUNNEL_HOST
            remote_stream_url = self._get_remote_stream_url(
                mapped_port, stream_url, remote_ip, ip_address, port
            )

            self.db.add_camera(
                {
                    "ip_address": ip_address,
                    "port_number": port,
                    "username": username,
                    "password": password,
                    "stream_url": stream_url,
                    "profile_token": profile_token,
                    "remote_stream_url": remote_stream_url,
                    "manufacturer": manufacturer,
                    "model": model,
                    "firmware_version": firmware_version,
                    "serial_number": serial_number,
                    "hardware_id": hardware_id,
                    "resolution": resolution,
                    "fps": fps,
                    "bitrate": bitrate,
                    "encoding": encoding,
                    "hostname": (hostname["Name"] or ""),
                }
            )

    def _get_remote_stream_url(
        self, mapped_port, stream_url, remote_ip, ip_address, port
    ):
        if mapped_port:
            remote_port = int(mapped_port[RemotePortMappingTableIndex.REMOTE_PORT])
            return self.tunnel_helper.change_address(stream_url, remote_ip, remote_port)
        else:
            remote_port = self.tunnel_helper.get_available_port()
            self.db.add_remote_port_mapping(
                {
                    "ip_address": ip_address,
                    "port_number": port,
                    "remote_port": remote_port,
                }
            )
            return self.tunnel_helper.change_address(stream_url, remote_ip, remote_port)
