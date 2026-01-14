from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


def _ventilation_rate(altitude_ft: float) -> float:
    altitude_m = altitude_ft * 0.3048
    altitude_above_1500_m = max(0.0, altitude_m - 1500.0)
    ventilation_increase_factor = altitude_above_1500_m / 1000.0
    ventilation_rate = 6.0 * (1.0 + ventilation_increase_factor)
    return min(ventilation_rate, 60.0)


def physiological_params(altitude_ft: float) -> Dict[str, float]:
    altitude_m = altitude_ft * 0.3048
    pressure_at_altitude = 760.0 * (1 - (2.25577e-5 * altitude_m)) ** 5.25588
    fio2 = 0.2095
    pio2 = (pressure_at_altitude - 47.0) * fio2
    pao2 = pio2 - 5.0
    sao2 = 100.0 * (pao2**3) / (pao2**3 + 150.0**3)

    ventilation_rate = _ventilation_rate(altitude_ft)
    altitude_above_1000_m = max(0.0, altitude_m - 1000.0)
    heart_rate_increase = altitude_above_1000_m / 100.0
    heart_rate = 70.0 + heart_rate_increase

    return {
        "altitude_ft": altitude_ft,
        "altitude_m": altitude_m,
        "pressure_mmHg": pressure_at_altitude,
        "pao2": pao2,
        "sao2": sao2,
        "ventilation_rate_l_min": ventilation_rate,
        "heart_rate_bpm": heart_rate,
    }


def gas_consumption(
    students_per_week: int,
    weeks: int,
    session_duration_min: float,
    recovery_duration_min: float,
    altitude_ft: float,
    price_air: float,
    price_nitrogen: float,
    price_oxygen: float,
    contingency: float,
) -> Dict[str, float]:
    ventilation_rate = _ventilation_rate(altitude_ft)
    air_consumed_session = (ventilation_rate * session_duration_min) / 1000.0
    nitrogen_consumed_session = air_consumed_session * 0.05
    oxygen_consumed_session = (ventilation_rate * recovery_duration_min) / 1000.0

    weekly_air = air_consumed_session * students_per_week
    weekly_nitrogen = nitrogen_consumed_session * students_per_week
    weekly_oxygen = oxygen_consumed_session * students_per_week

    total_air = weekly_air * weeks
    total_nitrogen = weekly_nitrogen * weeks
    total_oxygen = weekly_oxygen * weeks

    total_cost_air = total_air * price_air
    total_cost_nitrogen = total_nitrogen * price_nitrogen
    total_cost_oxygen = total_oxygen * price_oxygen
    total_cost = total_cost_air + total_cost_nitrogen + total_cost_oxygen

    return {
        "weekly_air_m3": weekly_air,
        "weekly_nitrogen_m3": weekly_nitrogen,
        "weekly_oxygen_m3": weekly_oxygen,
        "total_air_m3": total_air,
        "total_nitrogen_m3": total_nitrogen,
        "total_oxygen_m3": total_oxygen,
        "total_cost_air": total_cost_air,
        "total_cost_nitrogen": total_cost_nitrogen,
        "total_cost_oxygen": total_cost_oxygen,
        "total_cost": total_cost,
        "total_cost_with_contingency": total_cost * (1 + contingency),
    }


def cylinder_capacity(
    air_cyl_m3: float,
    nitrogen_cyl_m3: float,
    oxygen_cyl_m3: float,
    session_duration_min: float,
    recovery_duration_min: float,
    altitude_ft: float,
) -> Dict[str, float]:
    ventilation_rate = _ventilation_rate(altitude_ft)
    air_per_session = (ventilation_rate * session_duration_min) / 1000.0
    nitrogen_per_session = air_per_session * 0.05
    oxygen_per_session = (ventilation_rate * recovery_duration_min) / 1000.0

    max_students_air = int(air_cyl_m3 // air_per_session) if air_per_session else 0
    max_students_nitrogen = int(nitrogen_cyl_m3 // nitrogen_per_session) if nitrogen_per_session else 0
    max_students_oxygen = int(oxygen_cyl_m3 // oxygen_per_session) if oxygen_per_session else 0
    max_students = min(max_students_air, max_students_nitrogen, max_students_oxygen)

    return {
        "air_per_session_m3": air_per_session,
        "nitrogen_per_session_m3": nitrogen_per_session,
        "oxygen_per_session_m3": oxygen_per_session,
        "max_students_air": max_students_air,
        "max_students_nitrogen": max_students_nitrogen,
        "max_students_oxygen": max_students_oxygen,
        "max_students": max_students,
    }


def single_session(
    session_duration_min: float,
    recovery_duration_min: float,
    altitude_ft: float,
    price_air: float,
    price_nitrogen: float,
    price_oxygen: float,
) -> Dict[str, float]:
    ventilation_rate = _ventilation_rate(altitude_ft)
    air_consumed = (ventilation_rate * session_duration_min) / 1000.0
    nitrogen_consumed = air_consumed * 0.05
    oxygen_consumed = (ventilation_rate * recovery_duration_min) / 1000.0

    cost_air = air_consumed * price_air
    cost_nitrogen = nitrogen_consumed * price_nitrogen
    cost_oxygen = oxygen_consumed * price_oxygen
    total_cost = cost_air + cost_nitrogen + cost_oxygen

    return {
        "air_consumed_m3": air_consumed,
        "nitrogen_consumed_m3": nitrogen_consumed,
        "oxygen_consumed_m3": oxygen_consumed,
        "cost_air": cost_air,
        "cost_nitrogen": cost_nitrogen,
        "cost_oxygen": cost_oxygen,
        "total_cost": total_cost,
    }
