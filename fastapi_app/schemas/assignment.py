from pydantic import BaseModel, field_validator, model_validator, field_serializer
from typing import Optional, Union
from datetime import datetime
from decimal import Decimal


class AssignmentBase(BaseModel):
    tieu_de: str
    noi_dung: str
    han_nop: Optional[datetime] = None
    is_required: bool = False
    diem_toi_da: Optional[Decimal] = 10.0
    file_path: Optional[str] = None

    @field_validator('han_nop', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                # Parse ISO format: YYYY-MM-DDTHH:mm:ss hoặc YYYY-MM-DD
                if 'T' in v:
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                else:
                    # Nếu chỉ có date, thêm time 23:59:00
                    return datetime.fromisoformat(f"{v}T23:59:00")
            except Exception as e:
                # Nếu không parse được, trả về None
                return None
        return v

    @field_validator('diem_toi_da', mode='before')
    @classmethod
    def parse_decimal(cls, v):
        if v is None:
            return Decimal('10.0')
        if isinstance(v, (int, float, str)):
            try:
                return Decimal(str(v))
            except:
                return Decimal('10.0')
        return v


class AssignmentCreate(AssignmentBase):
    # khoa_hoc_id được lấy từ path parameter, không cần trong body
    pass


class AssignmentOut(AssignmentBase):
    id: int
    khoa_hoc_id: int
    created_at: Optional[datetime] = None
    diem_toi_da: Optional[Union[Decimal, float]] = 10.0

    @field_serializer('diem_toi_da')
    def serialize_diem_toi_da(self, value: Optional[Union[Decimal, float]]) -> Optional[float]:
        if value is None:
            return 10.0
        if isinstance(value, Decimal):
            return float(value)
        return float(value) if value else 10.0

    @field_validator('diem_toi_da', mode='before')
    @classmethod
    def parse_diem_toi_da(cls, v):
        if v is None:
            return 10.0
        if isinstance(v, Decimal):
            return float(v)
        return v

    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    noi_dung: Optional[str] = None
    file_path: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    bai_tap_id: int


class SubmissionOut(SubmissionBase):
    id: int
    bai_tap_id: int
    user_id: int
    diem: Optional[Decimal] = None
    nhan_xet: Optional[str] = None
    trang_thai: str
    ngay_nop: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True




