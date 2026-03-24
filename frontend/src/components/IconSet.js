import React from "react";

// Valid MUI icons
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import MedicalServicesIcon from "@mui/icons-material/MedicalServices";
import HealingIcon from "@mui/icons-material/Healing";

import PersonIcon from "@mui/icons-material/Person";
import GroupIcon from "@mui/icons-material/Group";
import BadgeIcon from "@mui/icons-material/Badge";

import HotelIcon from "@mui/icons-material/Hotel";
import EventSeatIcon from "@mui/icons-material/EventSeat";
import KingBedIcon from "@mui/icons-material/KingBed";

import DescriptionIcon from "@mui/icons-material/Description";
import AssignmentIcon from "@mui/icons-material/Assignment";
import HistoryIcon from "@mui/icons-material/History";

import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";

import LockIcon from "@mui/icons-material/Lock";
import VpnKeyIcon from "@mui/icons-material/VpnKey";
import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";

// Map keywords to icons
const icons = {
  hospital: LocalHospitalIcon,
  services: MedicalServicesIcon,
  healing: HealingIcon,

  patient: PersonIcon,
  patients: GroupIcon,
  doctor: BadgeIcon,

  bed: HotelIcon,
  seat: EventSeatIcon,
  icu: KingBedIcon,

  record: DescriptionIcon,
  assignment: AssignmentIcon,
  history: HistoryIcon,

  emergency: WarningAmberIcon,
  alert: NotificationsActiveIcon,
  warning: WarningAmberIcon,

  lock: LockIcon,
  key: VpnKeyIcon,
  verified: VerifiedUserIcon,
};

// IconSet component
const IconSet = ({ type, color = "inherit", size = "medium", ...props }) => {
  const ChosenIcon = icons[type] || LocalHospitalIcon; // fallback = hospital
  return <ChosenIcon color={color} fontSize={size} {...props} />;
};

export default IconSet;
