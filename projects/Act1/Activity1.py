#!/usr/bin/env python3
"""
Mini Expert System for Student Rules
- Attendance Rule
- Grading Rule
- Login System Rule
- Bonus Points Rule
- Library Borrowing Rule (NEW)
All outcomes are logged to logic_results.csv
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any, Tuple

import os

CSV_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "logic_results.csv")


def attendance_rule(attendance_pct: float) -> Tuple[bool, str]:
    """
    Attendance Rule:
    If attendance >= 75% -> Eligible; else -> Not eligible
    """
    ok = attendance_pct >= 75.0
    return ok, f"attendance={attendance_pct:.1f}% -> {'eligible' if ok else 'not eligible'}"

def grading_rule(final_grade: float) -> Tuple[bool, str]:
    """
    Grading Rule:
    If final grade >= 75 -> Passed; else -> Failed
    """
    ok = final_grade >= 75.0
    return ok, f"grade={final_grade:.1f} -> {'pass' if ok else 'fail'}"

def login_system_rule(username_ok: bool, password_ok: bool, is_locked: bool) -> Tuple[bool, str]:
    """
    Login System Rule:
    If username is valid AND password is valid AND account not locked -> Login success
    """
    ok = username_ok and password_ok and (not is_locked)
    detail = f"user_ok={username_ok}, pass_ok={password_ok}, locked={is_locked} -> {'login success' if ok else 'login denied'}"
    return ok, detail

def bonus_points_rule(participated: bool, base_score: float, bonus: float=5.0, cap: float=100.0) -> Tuple[bool, str]:
    """
    Bonus Points Rule:
    If student participated in an extra activity -> add bonus points (default +5, capped to 100)
    Returns True if bonus applied, else False
    """
    if participated:
        new_score = min(base_score + bonus, cap)
        return True, f"participated={participated}, base={base_score} -> bonus +{bonus}, final={new_score}"
    else:
        return False, f"participated={participated}, base={base_score} -> no bonus, final={base_score}"

def library_borrowing_rule(id_valid: bool, has_overdue: bool) -> Tuple[bool, str]:
    """
    NEW RULE — Library Borrowing:
    If ID is valid AND has no overdue items -> Allowed to borrow; else -> Not allowed
    """
    ok = id_valid and (not has_overdue)
    return ok, f"id_valid={id_valid}, overdue={has_overdue} -> {'allowed' if ok else 'not allowed'}"

def evaluate_student(student: Dict[str, Any]) -> Dict[str, Any]:
    results = {}
    a_ok, a_detail = attendance_rule(student['attendance_pct'])
    g_ok, g_detail = grading_rule(student['final_grade'])
    l_ok, l_detail = login_system_rule(student['username_ok'], student['password_ok'], student['is_locked'])
    b_ok, b_detail = bonus_points_rule(student['participated'], student['base_score'])
    lib_ok, lib_detail = library_borrowing_rule(student['id_valid'], student['has_overdue'])

    results['AttendanceRule'] = (a_ok, a_detail)
    results['GradingRule'] = (g_ok, g_detail)
    results['LoginSystemRule'] = (l_ok, l_detail)
    results['BonusPointsRule'] = (b_ok, b_detail)
    results['LibraryBorrowingRule'] = (lib_ok, lib_detail)

    return results

def log_results(student_name: str, results: Dict[str, Any], csv_path: str = CSV_PATH) -> None:
    fieldnames = [
        "timestamp","student",
        "AttendanceRule","AttendanceDetail",
        "GradingRule","GradingDetail",
        "LoginSystemRule","LoginDetail",
        "BonusPointsRule","BonusDetail",
        "LibraryBorrowingRule","LibraryDetail"
    ]
    # ensure file exists with header
    try:
        need_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    except Exception:
        need_header = True

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if need_header:
            writer.writeheader()
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "student": student_name,
            "AttendanceRule": results['AttendanceRule'][0],
            "AttendanceDetail": results['AttendanceRule'][1],
            "GradingRule": results['GradingRule'][0],
            "GradingDetail": results['GradingRule'][1],
            "LoginSystemRule": results['LoginSystemRule'][0],
            "LoginDetail": results['LoginSystemRule'][1],
            "BonusPointsRule": results['BonusPointsRule'][0],
            "BonusDetail": results['BonusPointsRule'][1],
            "LibraryBorrowingRule": results['LibraryBorrowingRule'][0],
            "LibraryDetail": results['LibraryBorrowingRule'][1],
        }
        writer.writerow(row)

def demo():
    test_students = [
        {
            "name": "Mendez",
            "attendance_pct": 82.5,
            "final_grade": 78.0,
            "username_ok": True,
            "password_ok": True,
            "is_locked": False,
            "participated": True,
            "base_score": 88.0,
            "id_valid": True,
            "has_overdue": False
        },
        {
            "name": "Mendoza",
            "attendance_pct": 70.0,
            "final_grade": 72.0,
            "username_ok": True,
            "password_ok": False,
            "is_locked": False,
            "participated": False,
            "base_score": 65.0,
            "id_valid": True,
            "has_overdue": True
        },
        {
            "name": "Mercado",
            "attendance_pct": 95.0,
            "final_grade": 92.0,
            "username_ok": True,
            "password_ok": True,
            "is_locked": True,
            "participated": True,
            "base_score": 96.0,
            "id_valid": False,
            "has_overdue": False
        }
    ]

    print("=== Mini Expert System — Demo Run ===")
    for s in test_students:
        results = evaluate_student(s)
        log_results(s["name"], results)
        print(f"\nStudent: {s['name']}")
        for rule, (ok, detail) in results.items():
            print(f" - {rule}: {ok} | {detail}")


if __name__ == "__main__":
    # ensure clean CSV for demo purposes (comment next two lines if you want to append across runs)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    demo()
