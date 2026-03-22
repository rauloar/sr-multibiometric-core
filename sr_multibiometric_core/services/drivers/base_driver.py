class BaseBiometricDriver:
    """
    Base class for all biometric device drivers.
    All drivers must implement these methods.
    """
    
    def __init__(self, device):
        self.device = device
        
    def connect(self):
        """Establish connection to the device."""
        raise NotImplementedError
        
    def disconnect(self):
        """Close connection to the device."""
        raise NotImplementedError
        
    def get_logs(self):
        """
        Pull attendance logs from the device.
        Returns a list of dicts suitable for biometric.log creation.
        """
        raise NotImplementedError
        
    def set_time(self):
        """Sync device clock with Odoo server time."""
        raise NotImplementedError
        
    def ping(self):
        """Test connection/reachability to the device."""
        raise NotImplementedError

    def get_device_info(self):
        """Return terminal metadata for UI display after connection tests."""
        raise NotImplementedError
