include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../modules/static-site"
}

inputs = {
  domain_name           = "soboappliancerepair.com"
  github_pages_username = "Kyle825"

  # Protonmail verification (from protonmail_verifications/protonMail.txt)
  protonmail_verification_txt = "protonmail-verification=2ecccd951a75bf45fdd74dbb8f3de73885013d2c"

  # DKIM CNAME records from Protonmail
  protonmail_dkim_cnames = {
    "protonmail._domainkey"  = "protonmail.domainkey.du7iztedrwjjm4w7smsba3i6lzzk6sqngpa62dfx4cscgecv2orua.domains.proton.ch."
    "protonmail2._domainkey" = "protonmail2.domainkey.du7iztedrwjjm4w7smsba3i6lzzk6sqngpa62dfx4cscgecv2orua.domains.proton.ch."
    "protonmail3._domainkey" = "protonmail3.domainkey.du7iztedrwjjm4w7smsba3i6lzzk6sqngpa62dfx4cscgecv2orua.domains.proton.ch."
  }
}
