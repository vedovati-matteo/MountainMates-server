from app import create_app

app = create_app('prod')
app.app_context().push()  # Push an application context to make `db` and `migrate` available