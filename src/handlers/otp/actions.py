from src.utils import get_current_time, set_exp_time, generate_otp
from src.events import NotificationServiceManager, Events
from src.models import Otp
from .queries import OtpQueries
from .responses import Codes, ResponseOtp


class OtpHandler(OtpQueries):

    def __init__(self,  lookup: str):
        """
        Initializes the OTPService with the specified service, lookup, and OTP type.

        Parameters:
        ----------
        lookup : str
            The lookup identifier for the user, typically an email or phone number.

        Raises:
        ------
        """
        self.service: NotificationServiceManager = NotificationServiceManager()
        self.lookup: str = lookup
        self.otp_type: str = self.service.service_type
        super().__init__()

    def send_otp(self) -> ResponseOtp:

        data: Otp | None = self._check_otp()

        if data:
            # check for existing otp is expired
            if get_current_time(strftime=False) < data.expiration_time:
                return ResponseOtp(Codes.ALREADY_EXISTS, info="Otp already sent.")

            self._delete_otp(otp_id=data.id)

        # create new otp
        otp_value = generate_otp()

        otp_object = Otp()
        otp_object.otp = otp_value
        if self.otp_type == 'mail':
            otp_object.email = self.lookup
        else:
            otp_object.phone_number = self.lookup

        self._create_new_otp(otp_object)

        otp_event = Events.OTP(otp=otp_value, emails=[self.lookup])
        self.service.send(otp_event)

        return ResponseOtp(Codes.DELIVERED, info="successfull")

    def resend_otp(self) -> ResponseOtp:

        data: Otp | None = self._check_otp()

        if data is None:
            return ResponseOtp(Codes.NOT_FOUND, info="record not found")

        if data.resend_attempts >= 5:
            timediff_seconds = int(
                (get_current_time(strftime=False) - data.updated_time).total_seconds())

            if timediff_seconds <= 120:
                return ResponseOtp(Codes.TOO_MANY_ATTEMPS, info=f"{120 - timediff_seconds}")

        otp_data = {
            'otp': generate_otp(),
            'expiration_time': set_exp_time(),
            'updated_time': get_current_time(),
            'resend_attempts': data.resend_attempts + 1
        }

        self._update_exp_time(data.id, **otp_data)

        otp_event = Events.OTP(otp=otp_data['otp'], emails=[self.lookup])
        self.service.send(otp_event)

        return ResponseOtp(Codes.DELIVERED, info="successfull")

    def verify_otp(self, otp) -> ResponseOtp:

        data: Otp | None = self._check_otp()

        if data is None:
            return ResponseOtp(Codes.NOT_FOUND, info="not found")

        if data.otp != otp:
            return ResponseOtp(Codes.INVALID, info="otp mismatch")

        if get_current_time(strftime=False) > data.expiration_time:
            return ResponseOtp(Codes.EXPIRED, info="otp expired")

        self._delete_otp(otp_id=data.id)

        return ResponseOtp(Codes.VERIFIED, info="successfull")
