import dropbox

dbx = dropbox.Dropbox('sl.AxHga4leivG3GDgBDUkIjqgUtAXokny517-FkuVAMFsiFmwE3INwJvFXdBx7rPKWaFs_GPPl8T7Bg4AZY3PqmrGupUCbQy7P_qU4KWvQ9b3sZ7xzCdOHmYK_mGc4AmIt7gdCiK4')
dbx.users_get_current_account()
for entry in dbx.files_list_folder('/UCU').entries:
    print(entry.name)

with open("Document.docx", "wb") as f:
    metadata, res = dbx.files_download(path='/UCU/Document.docx')
    f.write(res.content)
