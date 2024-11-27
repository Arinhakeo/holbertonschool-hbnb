from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

facade = HBnBFacade()

# Input and output models for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='Unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Update timestamp')
})

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.get_all_users()

    @api.doc('create_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new user"""
        try:
            return facade.create_user(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user by ID"""
        user = facade.get_user(user_id)
        if user is None:
            api.abort(404, f"User {user_id} not found")
        return user

    @api.doc('update_user')
    @api.expect(user_input_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        try:
            return facade.update_user(user_id, api.payload)
        except ValueError as e:
            api.abort(400, str(e))
            
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200


    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    def put(self, user_id):
            """Update a user by ID"""
            print(f"Received PUT request for user_id: {user_id}")
            user_data = api.payload
            print(f"Request payload: {user_data}")

            # Check if the user exists
            existing_user = facade.get_user(user_id)
            if not existing_user:
                return {'error': 'User not found'}, 404

            # Check for email uniqueness if the email is being changed
            if user_data['email'] != existing_user.email:
                duplicate_user = facade.get_user_by_email(user_data['email'])
                if duplicate_user:
                    return {'error': 'Email already registered'}, 400

            # Update the user's information
            existing_user.first_name = user_data['first_name']
            existing_user.last_name = user_data['last_name']
            existing_user.email = user_data['email']

            # Optionally, update the repository if using one
            facade.user_repo.update(existing_user.id, {
                'first_name': existing_user.first_name,
                'last_name': existing_user.last_name,
                'email': existing_user.email
            })
            return {
                'id': existing_user.id,
                'first_name': existing_user.first_name,
                'last_name': existing_user.last_name,
                'email': existing_user.email
            }, 200
