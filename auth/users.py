from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from ..models.users import UserCreate, UserBase, User, UserLogin
from ..models.token import Token, TokenData
from ..utils.db_utils import get_session
from ..utils.passw_utils import PasswordUtils
from ..utils.auth_utils import authenticate_user, generate_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"detail": "Invalid username or password"}},
)

ACCESS_TOKEN_EXPIRE_IN_DAYS = 15


@router.post('/login')
async def login(user_login: UserLogin, session: Session = Depends(get_session)) -> Token:
    """
    Get access Token
    Flow:
        1. check the email and password combination (authenticate)
        2. generate token (need to create a wrapper for it. using jose)
        3. return the token in json
    :return: access token
    """
    auth_success: bool = authenticate_user(session, user_login.email, user_login.password)
    if not auth_success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expiry: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_IN_DAYS)
    access_token: str = generate_token(data={"sub": user_login.email}, expires_delta=access_token_expiry)

    return Token(access_token=access_token, token_type="Bearer")


@router.post('/register')
async def register(
    user: UserCreate,
    session: Session = Depends(get_session)
) -> UserBase:
    """
    Flow:
        1. get email, full_name, password, confirm_password
        2. do validation of email, password and confirm_password
        3. save email, full_name, password in DB
            3.a. create a hash of password before saving in the db and save the hashed password
        4. return email, full_name in the response
    :return: json. Created User Details.
    """
    # Check if email already exists
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # cnf_pass check
    if user.confirm_password != user.password:
        raise HTTPException(status_code=400, detail="Password and Confirm Password mismatch")

    # Create new user
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        password=(PasswordUtils(passw=user.password).hash_passw()).decode('utf-8')
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
