from django.db import models

class Exchange(models.Model):
    cur_unit = models.CharField(max_length=100)
    cur_nm = models.CharField(max_length=100)
    ttb = models.FloatField()  # 송금받을 때 환율
    tts = models.FloatField()  # 송금보낼 때 환율
    deal_bas_r = models.FloatField()  # 기준 환율
    bkpr = models.CharField(max_length=100)
    yy_efee_r = models.CharField(max_length=100)
    ten_dd_efee_r = models.CharField(max_length=100)
    kftc_deal_bas_r = models.CharField(max_length=100)
    kftc_bkpr = models.CharField(max_length=100)

