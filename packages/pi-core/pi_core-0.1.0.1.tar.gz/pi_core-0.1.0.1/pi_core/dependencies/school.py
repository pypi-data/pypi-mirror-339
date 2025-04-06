from fastapi import Request, HTTPException


def get_current_school(request: Request) -> int:
    """
    Retrieves the current school ID from request.state.
    Set by SchoolContextMiddleware in pi-schools-app.
    """
    school_id = getattr(request.state, "school_id", None)
    if school_id is None:
        raise HTTPException(status_code=403, detail="Missing school context")
    return school_id