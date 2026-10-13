# -*- coding: utf-8 -*-
from extensions import db

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(60), nullable=False)
    qtd = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    preco_total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pendente', nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return 'Pedido %s - %s' % (self.id, self.product_name)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def get_by_id(self):
        try:
            res = db.session.query(Pedido).filter(Pedido.id == self.id).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
        return res

    def get_all(self):
        try:
            res = db.session.query(Pedido).order_by(Pedido.date_created.desc()).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
        return res

    def update_status(self, status):
        try:
            db.session.query(Pedido).filter(Pedido.id == self.id).update({'status': status})
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
