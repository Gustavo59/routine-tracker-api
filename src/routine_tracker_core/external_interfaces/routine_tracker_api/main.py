from routine_tracker_core.controllers import AuthenticationController
from routine_tracker_core.external_interfaces.routine_tracker_api import app_factory, login_manager
from routine_tracker_core.external_interfaces.routine_tracker_api.routers import routine

app = app_factory(title="Routine Tracker")


@app.get("/health", include_in_schema=False)
def health():
    return {"message": "OK"}


@app.post("/auth/", tags=["Authentication"])
def authentication(request: dict):
    controller = AuthenticationController(login_manager=login_manager)
    return controller.authenticate(request)


app.include_router(routine.router)
