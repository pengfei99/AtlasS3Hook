from atlas_s3_hook.S3Scanner import S3Scanner


def test_is_ignored_positive():
    assert S3Scanner.is_ignored(".keep")


def test_is_ignored_negative():
    assert not S3Scanner.is_ignored("keep")
