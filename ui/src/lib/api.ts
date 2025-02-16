import axios, { type AxiosResponse } from 'axios';

const rootPath = '/api';

const axi = axios.create({
  baseURL: rootPath
});

// TODO: ADD ZOD SCHEMA FOR TYPES
export const getUserCheckins = (user: string) =>
  axi.get(`checkins/user/${user}`, { params: { page: 1, size: 90 } });

export const getUsers = () => axi.get('checkins/users');
