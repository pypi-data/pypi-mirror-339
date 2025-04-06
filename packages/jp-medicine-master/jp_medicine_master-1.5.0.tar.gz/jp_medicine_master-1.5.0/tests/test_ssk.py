from pathlib import Path

import pytest
import jp_medicine_master as jpmed


#
# 医薬品マスター (ssk_y)
#
@pytest.mark.filterwarnings("ignore:Use `.*_y` instead")
def test_download_ssk_y_all():
    save_dir = Path.home() / '.jp_medicine_master'
    if not save_dir.is_dir():
        save_dir.mkdir()

    years = jpmed.get_years_ssk_y()
    for year in years:
        filepath = jpmed.download_ssk_y(save_dir=save_dir, year=year)
        assert filepath


@pytest.mark.filterwarnings("ignore:Use `.*_y` instead")
def test_read_ssk_y():
    df = jpmed.read_ssk_y()

    # ヘッダー行
    assert len(df.columns) == 42
    assert df.columns[0] == '変更区分'

    # 行数 ~ 20,000
    assert 18_000 <= len(df) <= 22_000


@pytest.mark.filterwarnings("ignore:Use `.*_y` instead")
def test_read_ssk_y_with_file_info():
    df = jpmed.read_ssk_y(file_info=True)

    # ヘッダー行
    assert len(df.columns) == 43
    assert df.columns[-1] == 'file'
