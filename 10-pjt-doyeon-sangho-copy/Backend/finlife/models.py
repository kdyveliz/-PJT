from django.db import models

# 예금 상품 모델
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    JOIN_DENY_CHOICES = [
        (1, '제한없음'),
        (2, '서민전용'),
        (3, '일부제한'),
    ]
    join_deny = models.IntegerField(choices=JOIN_DENY_CHOICES, default=1)  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대 조건
    dcls_month = models.CharField(max_length=6, null=True, blank=True)  # 공시월 (YYYYMM)
    dcls_strt_day = models.DateField(null=True, blank=True)  # 공시 시작일
    dcls_end_day = models.DateField(null=True, blank=True)  # 공시 종료일
    fin_co_subm_day = models.DateField(null=True, blank=True)  # 금융회사 제출일


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 관련 금융상품
    fin_prdt_cd = models.TextField()  # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 금리 유형 명칭
    intr_rate = models.FloatField()  # 기본 이율
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대 이율
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)


# 적금 상품 모델
class SavingsProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    mtrt_int = models.TextField(blank=True, null=True)  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대 조건
    join_deny = models.IntegerField(
        choices=[
            (1, '제한없음'),
            (2, '서민전용'),
            (3, '일부제한'),
        ],
        default=1,
    )  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    max_limit = models.BigIntegerField(null=True, blank=True)  # 최고 한도
    dcls_month = models.CharField(max_length=6, null=True, blank=True)  # 공시월 (YYYYMM)
    dcls_strt_day = models.DateField(null=True, blank=True)  # 공시 시작일
    dcls_end_day = models.DateField(null=True, blank=True)  # 공시 종료일
    fin_co_subm_day = models.DateField(null=True, blank=True)  # 금융회사 제출일


class SavingsOptions(models.Model):
    product = models.ForeignKey(SavingsProducts, on_delete=models.CASCADE)  # 관련 적금상품
    fin_prdt_cd = models.TextField()  # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 금리 유형 명칭
    intr_rate = models.FloatField()  # 기본 이율
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대 이율
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)
