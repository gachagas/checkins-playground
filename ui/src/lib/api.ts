import axios, { type AxiosResponse } from 'axios';

const rootPath = '/api';

const axi = axios.create({
  baseURL: rootPath
});

export const getUsers = () => axi.get('checkins/users');
