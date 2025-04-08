from .constants import CHAR_ARRAY, LONG_PTR, UTF_ENCODING
from .core_base import CoreBase, ffi

ffi.cdef(
    """
    long __stdcall IV_open();
    long __stdcall IV_close();
    long __stdcall IV_MaxDevices();
    long __stdcall IV_selectdevice(long *devnr);
    long __stdcall IV_getdevicestatus();
    long __stdcall IV_readSN(char *sntext);
    long __stdcall IV_connect(long* devconnect);
    long __stdcall IV_VersionHost(long *version);
    long __stdcall IV_VersionDll();
    long __stdcall IV_VersionCheck();
    long __stdcall IV_HostHandle();
    long __stdcall IV_VersionDllFile();
    long __stdcall IV_VersionDllFileStr();
    long __stdcall IV_SelectChannel(long *channel);
    long __stdcall IV_SelectSn(char *sntext);
    long __stdcall IV_getDbFileName(char *fname);
"""
)


class GenericFunctions(CoreBase):
    @staticmethod
    def IV_open() -> int:
        """Open the driver to manipulate the Ivium software"""
        CoreBase.set_driver_open(True)
        return CoreBase.get_lib().IV_open()

    @staticmethod
    def IV_close() -> int:
        """Closes the iviumSoft driver"""
        CoreBase.set_driver_open(False)
        return CoreBase.get_lib().IV_close()

    @staticmethod
    def IV_MaxDevices() -> int:
        """Returns the maximum number of devices that can be managed by IviumSoft"""
        return CoreBase.get_lib().IV_MaxDevices()

    @staticmethod
    def IV_selectdevice(iviumsoft_instance_number: int = 1) -> tuple[int, int]:
        """It allows to select one instance of the currently running IviumSoft instances"""
        instance_number_ptr = ffi.new(LONG_PTR, iviumsoft_instance_number)
        result_code = CoreBase.get_lib().IV_selectdevice(instance_number_ptr)
        return result_code, instance_number_ptr[0]

    @staticmethod
    def IV_getdevicestatus() -> int:
        """It returns -1 (no IviumSoft), 0 (not connected), 1 (available_idle), 2 (available_busy),
        3 (no device available)"""
        return CoreBase.get_lib().IV_getdevicestatus()

    @staticmethod
    def IV_readSN() -> tuple[int, str]:
        """Returns the serial number of the currently selected device"""
        device_serial_number_ptr = ffi.new(CHAR_ARRAY, 16)
        result_code = CoreBase.get_lib().IV_readSN(device_serial_number_ptr)
        return result_code, ffi.string(device_serial_number_ptr).decode(UTF_ENCODING)

    @staticmethod
    def IV_connect(connection_status: int) -> tuple[int, int]:
        """It connects the currently selected device"""
        connection_status_ptr = ffi.new(LONG_PTR, connection_status)
        result_code = CoreBase.get_lib().IV_connect(connection_status_ptr)
        return result_code, connection_status_ptr[0]

    @staticmethod
    def IV_VersionHost(version_host: int) -> tuple[int, int]:
        """REVISE!!! Returns the version Host"""
        version_host_ptr = ffi.new(LONG_PTR, version_host)
        result_code = CoreBase.get_lib().IV_VersionHost(version_host_ptr)
        return result_code, version_host_ptr[0]

    @staticmethod
    def IV_VersionDll() -> int:
        """Returns the version of the IviumSoft dll"""
        return CoreBase.get_lib().IV_VersionDll()

    @staticmethod
    def IV_VersionCheck() -> int:
        """It returns 1 if the selected instance of IviumSoft is running"""
        return CoreBase.get_lib().IV_VersionCheck()

    @staticmethod
    def IV_HostHandle() -> int:
        """REVISE!!! Returns Host Handle"""
        return CoreBase.get_lib().IV_HostHandle()

    @staticmethod
    def IV_VersionDllFile() -> int:
        """REVISE!!! Returns DLL file version"""
        return CoreBase.get_lib().IV_VersionDllFile()

    @staticmethod
    def IV_VersionDllFileStr() -> str:
        """REVISE!!! Returns DLL file version str"""
        return CoreBase.get_lib().IV_VersionDllFileStr()

    @staticmethod
    def IV_SelectChannel(channel_number: int) -> int:
        """Selects a channel:
        - if not yet active, the [int] number of tabs is automatically opened and
          the [int] tab becomes active.
        - if Ivium-n-Soft is active already, the [int] tab becomes active.
        Now the channel/instrument that is connected to this tab can be controlled.
        If no instrument is connected, the next available instrument in the list can
        be connected (IV_connect) and controlled."""
        channel_number_ptr = ffi.new(LONG_PTR, channel_number)
        result_code = CoreBase.get_lib().IV_SelectChannel(channel_number_ptr)
        return result_code

    @staticmethod
    def IV_SelectSn(serial_number: str) -> tuple[int, str]:
        """Selects device by serial number from the list of available devices to connect"""
        serial_number_ptr = ffi.new(CHAR_ARRAY, serial_number.encode(UTF_ENCODING))
        result_code = CoreBase.get_lib().IV_SelectSn(serial_number_ptr)
        return result_code, ffi.string(serial_number_ptr).decode(UTF_ENCODING)

    @staticmethod
    def IV_getDbFileName():
        """Selects device by serial number from the list of available devices to connect"""
        db_path_ptr = ffi.new(CHAR_ARRAY, 16)
        result_code = CoreBase.get_lib().IV_getDbFileName(db_path_ptr)
        return result_code, ffi.string(db_path_ptr).decode(UTF_ENCODING)
