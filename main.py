import ship_that_stinks
import config

app = ship_that_stinks.create_app(config)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
