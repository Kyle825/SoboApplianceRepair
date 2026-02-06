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

  # DKIM CNAME records — fill these in from Protonmail's custom domain wizard.
  # After adding your domain in Protonmail, they'll provide 3 CNAME values.
  # Uncomment and populate, then run `terragrunt apply` again.
  #
  # protonmail_dkim_cnames = {
  #   "protonmail._domainkey"  = "protonmail._domainkey.xxxxx.domains.proton.ch."
  #   "protonmail2._domainkey" = "protonmail2._domainkey.xxxxx.domains.proton.ch."
  #   "protonmail3._domainkey" = "protonmail3._domainkey.xxxxx.domains.proton.ch."
  # }
}
