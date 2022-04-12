import ast

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('data/users.csv')  # read the local CSV
        data = data.to_dict()  # convert the data to dictionary
        return {'data': data}, 200  # return the data and OK Code

    def post(self):
        parser = reqparse.RequestParser()  # initial
        parser.add_argument('userId', requried=True)  # adding arguments
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()  # parse the arguments to dict

        # read the CSV file
        data = pd.read_csv('data/users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 409
        else:
            # create the new dataframe with new values
            new_data = pd.DataFrame({
                'userId': [args['userId']],
                'name': [args['name']],
                'city': [args['city']],
                'locations': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('data/users.csv', index=False)  # save the CSV file
            return {'data': data.to_dict()}, 200  # return status CODE OK

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        # read the CSV file
        data = pd.read_csv('data/users.csv')

        if args['userId'] in list(data['userId']):
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select the user
            user_data = data[data['userId'] == args['userId']]

            # update location
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

            # save back the CSV
            data.to_csv('users.csv', index=False)
            # return data and OK Code
            return {'data': data.to_dict()}, 200
        else:
            # otherwise return that the user does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


api.add_resource(Users, '/users')  # '/users' is the endpoint for Users

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
