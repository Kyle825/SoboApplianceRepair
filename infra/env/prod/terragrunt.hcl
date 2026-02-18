include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../modules/static-site"
}

inputs = {
  domain_name           = "soboappliancerepair.com"
  github_pages_username = "Kyle825"

  # Google Workspace domain verification
  google_workspace_verification_txt = "google-site-verification=qklKPN8_oXRx44ZnBGpzdEpoGqfa1wJwO50qbgaat3g"

  # Google Workspace CNAME verification (alternative to TXT)
  google_workspace_verification_cname = {
    name  = "sh4ui3bf5uje"
    value = "gv-lunwduuauggg3k.dv.googlehosted.com"
  }

  # Google Workspace DKIM
  google_workspace_dkim_txt = "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuUShseB5w87pXPH/k63rvPnwAdjaQRC32rR7obk7cb9K2GJyZzLPYKxJwA3Qf3Yhx/jh65U4k9dAVqMrTy0/nggHy5Lt2IJ+qpsR2Jxu5b/yyNrgw2ClGbgd8p1tJeZaKcT9QVLEL+IDCTydIC6Jr0Go41JSF9VcXh80kdVdebvcZO4IukkorO723PFkjUf4ite771EFt6/LSwb1dQodBWSpa4hQoJ0Di/H05fz89YsKL5tiNrMPhjk66YpKhsgfuB9vtcI5ZMwX15Qk3PJzgtr7mqZtnOuVOiXerMqSADTn5teLXgaMyqh9LpDkMsEo+pQD0/yO/Oy9UP+tvWNNFwIDAQAB"

  # Google Search Console verification
  google_site_verification_txt = "google-site-verification=FmQn8kFt4GbAsVCXDGia2-PN1gn9eofg3HWkQVPAKwk"
}
