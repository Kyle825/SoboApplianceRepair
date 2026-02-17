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

  # Google Search Console verification
  google_site_verification_txt = "google-site-verification=FmQn8kFt4GbAsVCXDGia2-PN1gn9eofg3HWkQVPAKwk"
}
