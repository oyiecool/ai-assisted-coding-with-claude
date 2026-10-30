@app.get("/orders")
def list_orders(page: int = 1, size: int = 50, db=Depends(get_db),
                user=Depends(current_user)):
    offset = (page - 1) * size
    rows = db.execute(
        text("SELECT * FROM orders ORDER BY created_at DESC "
             "LIMIT :size OFFSET :offset"),
        {"size": size, "offset": offset},
    ).fetchall()
    return {"page": page, "items": [dict(r) for r in rows]}
