import {all, call, put, takeEvery} from 'redux-saga/effects';
import AuthApi from '../../api/AuthApi';
import * as Actions from '../actions/AuthActions';
import * as ProfileActions from '../actions/ProfileActions';
import * as Types from '../actions/AuthActionTypes';
import UserSession from '../../UserSession';
import {l} from "../../utils/GGGGGGG";

export default function* authFlow() {
    yield all([
        takeEvery(Types.LOGIN, login),
        takeEvery(Types.LOGOUT, logout)
    ]);
}

function* login(action) {
    var {username, password} = action;
    try {
        const response = yield call(AuthApi.login, username, password);
        l("success111111111",response);



        UserSession.setToken(response.token);

        yield put(Actions.loginSuccess(response.token));
        yield put(ProfileActions.getProfile());
    } catch (error) {

        l("error222222222",error);
        yield put(Actions.loginFailure(error));
    }
}

function* logout() {
    yield UserSession.setToken(null);
}
