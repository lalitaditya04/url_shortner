from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

    import os

    port = int(os.environ.get("PORT", 8000))  # 8000 for local, Cloud Run sets PORT automatically
    app.run(host="0.0.0.0", port=port)
