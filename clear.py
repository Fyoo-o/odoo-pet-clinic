bundles = env['ir.attachment'].search([('url', '=like', '/web/assets/%')])
bundles.unlink()
env.cr.commit()
print("Assets cleared successfully.")
