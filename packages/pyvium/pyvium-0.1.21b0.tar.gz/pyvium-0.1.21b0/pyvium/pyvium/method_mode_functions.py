from ..core import Core
from ..pyvium_verifiers import PyviumVerifiers


class MethodModeFunctions():
    @staticmethod
    def load_method(method_file_path: str):
        '''Loads method procedure previously saved to a file.
            method_file_path represents the full path to the file.'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        result_code, _ = Core.IV_readmethod(method_file_path)

        if result_code == 1:
            raise FileNotFoundError

    @staticmethod
    def save_method(method_file_path: str):
        '''Saves currently loaded method procedure to a file.
            method_file_path represents the full path to the new file.'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        Core.IV_savemethod(method_file_path)

    @staticmethod
    def start_method(method_file_path=''):
        '''Starts a method procedure.
            If method_file_path is an empty string then the presently loaded procedure is started.
            If the full path to a previously saved method is provided
            then the procedure is loaded from the file and started.'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()
        PyviumVerifiers.verify_device_is_connected_to_iviumsoft()
        PyviumVerifiers.verify_device_is_available()

        result_code, _ = Core.IV_startmethod(method_file_path)

        if result_code == 1:
            raise FileNotFoundError

    @staticmethod
    def abort_method():
        '''Aborts the ongoing method procedure'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()
        PyviumVerifiers.verify_device_is_connected_to_iviumsoft()

        Core.IV_abort()

    @staticmethod
    def save_data(data_file_path: str):
        '''Saves the results of the last method execution into a file.
            data_file_path represents the full path to the new file.
           IMPORTANT: If the path provided is not valid,
           it will close the selected iviumsoft instance.
        '''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        Core.IV_savedata(data_file_path)

    @staticmethod
    def set_method_parameter(parameter_name: str, parameter_value: str):
        '''Allows updating the parameter values for the currently loaded method procedrue.
            It only works for text based parameters and dropdowns (multiple option selectors).'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        Core.IV_setmethodparameter(
            parameter_name, parameter_value)

    @staticmethod
    def get_available_data_points_number():
        '''Returns actual available number of datapoints: indicates the progress during a run'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        _, available_data_points_number = Core.IV_Ndatapoints()

        return available_data_points_number

    @staticmethod
    def get_data_point(data_point_index: int):
        '''Get the data from a datapoint with index int, returns 3 values that depend on
            the used technique. For example LSV/CV methods return (E/I/0) Transient methods
            return (time/I,E/0), Impedance methods return (Z1,Z2,freq) etc.'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        _, value1, value2, value3 = Core.IV_getdata(
            data_point_index)

        return value1, value2, value3

    @staticmethod
    def get_data_point_from_scan(data_point_index: int, scan_index: int):
        '''Same as get_data_point, but with the additional scan_index parameter.
            This function will allow reading data from non-selected (previous) scans.'''
        PyviumVerifiers.verify_driver_is_open()
        PyviumVerifiers.verify_iviumsoft_is_running()

        _, value1, value2, value3 = Core.IV_getdatafromline(
            data_point_index, scan_index)

        return value1, value2, value3
