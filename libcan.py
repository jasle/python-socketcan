impor://github.com/awearness/clt15-infoscreent socket
import struct

class bcm_timeval:
	int tv_sec #long
	int tv_usec #long

class bcm_msg_head:



class can:
# CAN frame packing/unpacking (see 'struct can_frame' in <linux/can.h>)

	def __init__(self, interface):
		self._can_frame_fmt = "=IB3x8s"
		self._can_frame_size = struct.calcsize(can_frame_fmt)
		self._bcm_msg_head_fmt = "=3I4l2I"
		self._bcm_msg_head_size = struct.calcsize(bcm_msg_head_fmt)
		self._s = socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_BCM)
		self._s.connect((interface,))


	def __del__(self):
		print('TBD')

	def _build_can_frame(self, can_id, data):
		dlc = len(data)
		data = data.ljust(8, b'\x00')
		return struct.pack(self._frame_fmt, can_id, dlc, data)

	def _dissect_can_frame(self, frame):
		can_id, dlc, data = struct.unpack(self._frame_fmt, frame)
		return (can_id, dlc, data[:can_dlc])

	def _build_bcm_frame(self, command, settimmer=False, starttimmer=False, tx_countevt=False, tx_announce=False, tx_cp_can_id=False, rx_filter_id=False, rx_check_dlc=False, rx_no_autotimmer=False, rx_announce_resume=False, tx_reset_multi_idx=False, rx_rtr_frame=False, count, ival1_sec, ival1_usec, ival2_sec, ival2_usec, can_id, can_frames=[]):
		#Setting opcodke
		opcodes = {'tx_setup': 1, 'tx_delete': 2, 'tx_read': 3, 'tx_send': 4, 'rx_setup': 5, 'rx_delete': 6, 'rx_read': 7, 'tx_status': 8, 'tx_expired': 9, 'rx_status': 10, 'rx_timeout': 11, 'rx_chnaged': 12}
		opcode = opcodes[command]

		#Setting flags
		flags = 0
		flags = flags | 2**1 if settimmer==True
		flags = flags | 2**2 if starttimmer==True
		flags = flags | 2**3 if tx_countevt==True
		flags = flags | 2**4 if tx_announce==True
		flags = flags | 2**5 if tx_cp_can_id==True
		flags = flags | 2**6 if rx_filter_id==True
		flags = flags | 2**7 if rx_check_dlc==True
		flags = flags | 2**8 if rx_no_autotimmer==True
		flags = flags | 2**9 if rx_announce_resume==True
		flags = flags | 2**10 if tx_reset_multi_idx==True
		flags = flags | 2**11 if rx_rtr_frame==True

		nframes = len(can_frames)

		bcm_frame = struct.pack('=3I4l2I', opcode, flags, count, ival1_sec, ival1_usec, ival2_sec, ival2_usec, can_id, nframes)
		for frame in can_frames:
			bcm_frame = bcm_frame + _build_can_frame(frame)
		return bcm_frame


	def _dissect_bcm_frame_header(self, frame):
		opcode, flags, count, ival1_sec, ival1_usec, ival2_sec, ival2_usec, can_id, nframes = struct.unpack('=3I4l2I', frame)

		#Getting command
		commands = ['tx_setup', 'tx_delete', 'tx_read', 'tx_send', 'rx_setup', 'rx_delete', 'rx_read', 'tx_status', 'tx_expired', 'rx_status', 'rx_timeout', 'rx_chnaged']
		command = commands[opcode]

		#Getting flags
		settimmer = True if (flags & 2**1) != 0 else False
		starttimmer = True if (flags & 2**2) != 0 else False
		tx_countevt = True if (flags & 2**3) != 0 else False
		tx_announce = True if (flags & 2**4) != 0 else False
		tx_cp_can_id = True if (flags & 2**5) != 0 else False
		rx_filter_id = True if (flags & 2**6) != 0 else False
		rx_check_dlc = True if (flags & 2**7) != 0 else False
		rx_no_autotimmer = True if (flags & 2**8) != 0 else False
		rx_announce_resume = True if (flags & 2**9) != 0 else False
		tx_reset_multi_idx = True if (flags & 2**10) != 0 else False
		rx_rtr_frame = True if (flags & 2**11) != 0 else False

		return command, settimmer, starttimmer, tx_countevt, tx_announce, tx_cp_can_id, rx_filter_id, rx_check_dlc, rx_no_autotimmer, rx_announce_resume, tx_reset_multi_idx, rx_rtr_frame, count, ival1_sec, ival1_usec, ival2_sec, ival2_usec, can_id, nframes

	def _dissect_bcm_frame_data(self, nframes, frames):
		can_frames = []
		for n in range(nframes):
			can_id, can_dlc, data = _dissect_can_frame(frames[16*n:16*(n+1)])
			can_frames.append({'can_id': can_id, 'can_dlc': can_dlc, 'data': data})
		return can_frames

	def _send_bcm_frame(self, frame):
		pass

	def tx_setup(self, tdb):
		pass

	def tx_delete(self, can_id):
		pass

	def tx_read(self, can_id):
		pass

	def tx_send(self, can_id, data):
		pass

	def rx_setup(self, tbd):
		pass

	def rx_delete(self, tbd):
		pass

	def rx_read(self, tbd):
		pass
