import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

def get_driver(device):
    """
    Factory method to instantiate the correct driver based on device_type.
    """
    if not device:
        raise ValueError("Device is required to instantiate driver.")
        
    if device.ip == '192.168.1.200':
        from odoo.addons.sr_multibiometric_zkteco.drivers.fake_zk_driver import FakeZKDriver
        return FakeZKDriver(device)

    device_type = device.device_type
    
    if device_type == 'zkteco':
        try:
            from odoo.addons.sr_multibiometric_zkteco.drivers.zkteco_driver import ZKTecoDriver
            return ZKTecoDriver(device)
        except ImportError as e:
            _logger.error(f"Failed to load ZKTecoDriver: {e}")
            raise UserError("ZKTeco driver module is not available or not installed correctly.")

    if device_type == 'hikvision':
        try:
            from odoo.addons.sr_multibiometric_hikvision.drivers.hikvision_driver import HikvisionDriver
            return HikvisionDriver(device)
        except ImportError as e:
            _logger.error(f"Failed to load HikvisionDriver: {e}")
            raise UserError("Hikvision driver module is not available or not installed correctly.")
            
    # Raise error if driver type is not match
    raise NotImplementedError(f"Driver for device type '{device_type}' is not implemented.")
