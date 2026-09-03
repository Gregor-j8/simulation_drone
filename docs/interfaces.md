# sim ↔ FCS interface (draft)

Transport: **UDP on 127.0.0.1**, lockstep. Sim binds `:14650`, FCS binds `:14660`.
Encoding: packed little-endian POD structs, 8-byte header. Python mirror uses
`struct`. Schema version bump on any layout change.

```
Header      { uint32 magic=0xD5011E; uint16 msg_type; uint16 schema_ver; }

SensorFrame (sim → FCS)   msg_type=1
  uint64  sim_time_us
  uint32  seq
  Imu     imu[3]      // { float ax,ay,az (m/s^2); float gx,gy,gz (rad/s); uint8 healthy }
  Gps     gps[2]      // { double lat,lon; float alt_m; float vn,ve,vd; uint8 fix; uint8 sats }
  float   baro_alt_m
  float   mag[3]
  float   battery_v
  float   rc[8]        // normalized channels, NaN if no link

ActuatorFrame (FCS → sim)  msg_type=2
  uint64  fcs_time_us
  uint32  seq          // echoes SensorFrame.seq it responds to
  float   motor[4]     // [0,1]
  uint8   armed
  uint8   flight_mode  // enum
  uint8   fault_flags

FcsStatus (FCS → sim, optional, for logging)  msg_type=3
  uint64  fcs_time_us
  float   att_est[3]   // roll,pitch,yaw (rad)
  float   pos_est[3]   // NED (m)
  float   vel_est[3]   // NED (m/s)
  uint16  active_reqs  // bitfield of failsafe conditions
```

Lockstep protocol:
1. Sim integrates one physics step to `sim_time_us`.
2. Sim sends `SensorFrame(seq=n)`, blocks.
3. FCS runs one loop tick, replies `ActuatorFrame(seq=n)`.
4. Sim applies `motor[]`, advances. Timeout → sim aborts the run (test failure).

`WallClock` mode: FCS ignores lockstep pacing and instead sleeps to hold the tick
period, recording actual vs nominal tick time for the jitter histogram.
