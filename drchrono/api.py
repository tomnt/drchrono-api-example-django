from drchrono.endpoints import DoctorEndpoint, PatientEndpoint, AppointmentProfileEndpoint, AppointmentEndpoint, OfficeEndpoint

class Api:

    def __init__(self, access_token):
        self.access_token = access_token

    def __get_list(self, generator_obj):
        lv = []
        for i in generator_obj:
            lv.append(i)
        return lv

    def patients_list(self, params=None, **kwargs):
        """ Obtains patients list
            https://toms.drchrono.com/api-docs/#operation/patients_list
        Args:
            params (dict, optional):
            chart_id: string (chart_id)
            cursor: string (Cursor): The pagination cursor value.
            date_of_birth: string (date_of_birth)
            doctor  : integer (doctor)
            email   : string (email)
            ethnicity: string (ethnicity)
            first_name: string (first_name)
            gender  : string (gender)
            last_name: string (last_name)
            page_size: integer (Page size): Number of results to return per page.
            preferred_language: string (preferred_language)
            race    : string (race)
            since	: string (since)
        Returns:
            list: Patients list
        """
        #access_token = self.get_token()
        api = PatientEndpoint(self.access_token)
        g = api.list(params, **kwargs)
        return self.__get_list(g)

    def appointment_profiles_list(self,  params=None, **kwargs):
        """ Obtains profiles list
            https://toms.drchrono.com/api-docs/#operation/appointment_profiles_list
        Args:
            params (dict, optional):
                cursor	: string (Cursor): The pagination cursor value.
                doctor	: integer (doctor)
                page_size	: integer (Page size): Number of results to return per page.
        Returns:
            list: Profiles list
        """
        #access_token = self.get_token()
        api = AppointmentProfileEndpoint(self.access_token)
        g = api.list(params, **kwargs)
        return self.__get_list(g)
        # return next(api.list(params, kwargs))

    def appointments_list(self, params=None, date=None, start=None, end=None, **kwargs):
        """ Obtains Appointments list
            https://app.drchrono.com/api-docs/#operation/appointments_list
        Args:
            params (dict, optional):
                cursor	: string (Cursor): The pagination cursor value.
                date	: string (date)
                date_range	: string (date_range)
                doctor	: integer (doctor)
                office	: integer (office)
                page_size: integer (Page size): Number of results to return per page.
                patient	: integer (patient)
                since	: string (since)
                status	: string (status)            
            date (string, optional): Date
            start (string, optional): Start
            end (string, optional):  End
        Returns:
            list: appointments list
        """
        #access_token = self.get_token()
        api = AppointmentEndpoint(self.access_token)
        g = api.list(params, date, start, end, **kwargs)
        return self.__get_list(g)

    def appointments_update(self, id, data, partial=True, **kwargs):
        """ Updates an appointment
            https://app.drchrono.com/api-docs/#operation/appointments_partial_update
        Args:
            id (int): Appointment id. Example: id = 174509207
            data (dict): Data to update. Example: data = {"scheduled_time": "2021-05-06T10:39:00"}
            partial (bool, optional): Defaults to True.
        """
        #access_token = self.get_token()
        api = AppointmentEndpoint(self.access_token)
        api.update(id, data, partial=True, **kwargs)

    def appointments_create(self, params=None, **kwargs):
        """ Obtains Appointments list
            https://app.drchrono.com/api-docs/#operation/appointments_create
        Args:
            params (dict, optional):
                date:	string (date)
                date_range:	string (date_range)
                doctor:	integer (doctor)
                office:	integer (office)
                patient:	integer (patient)
                since:	string (since)
                status:	string (status)
            date (string, optional): Date
            start (string, optional): Start
            end (string, optional):  End
        Returns:
            list: appointments list
        """
        api = AppointmentEndpoint(self.access_token)
        #api.create(params, date, start, end, **kwargs)
        api.create(params, **kwargs)


    def offices_read(self, params=None, **kwargs):
        """ Obtains patients list
            https://toms.drchrono.com/api-docs/#operation/patients_list
        Args:
            params (dict, optional):
                cursor	: string (Cursor): The pagination cursor value.
                doctor	: integer (doctor)
                page_size	:integer (Page size):Number of results to return per page.
        Returns:
            list: Patients list
        """
        api = OfficeEndpoint(self.access_token)
        return next(api.list())

    
        # g = api.list(params, **kwargs)
        # return self.__get_list(g)