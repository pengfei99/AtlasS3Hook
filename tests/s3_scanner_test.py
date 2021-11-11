from atlas_s3_hook.S3Scanner import S3Scanner


def test_is_ignored_point_positive():
    assert S3Scanner.is_ignored(".keep")


def test_is_ignored_dash_positive():
    assert S3Scanner.is_ignored("_keep")


def test_is_ignored_negative():
    assert not S3Scanner.is_ignored("keep")


def test_is_ignored_with_full_path_point_positive():
    assert S3Scanner.is_ignored("toto/titi/.keep")


def test_is_ignored_with_full_path_dash_negative():
    assert S3Scanner.is_ignored("toto/titi/_keep")


def test_is_ignored_with_full_path_negative():
    assert not S3Scanner.is_ignored("toto/titi/keep")
