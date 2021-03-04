from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services

orm.start_mappers()
Session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = Session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"]
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return jsonify({"batchref": batchref}), 201
