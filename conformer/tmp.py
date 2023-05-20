import nemo.collections.asr as nemo_asr

temp_cn = nemo_asr.models.EncDecCTCModelBPE.restore_from('/home/user/code/data/sbb_test/manifest.json')
temp_cn.summarize()
