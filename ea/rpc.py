""" Battlefield 2142 stats querier

This is the python module package for querying EA's stat servers.

Please read the README

Copyright © 2006 Alexander Bondarenko <wiz@aenor.ru>

Licence:

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
"""

STELLA = 'stella.prod.gamespy.com'
BFWEB = 'bf2142web.gamespy.com'

from auth import make_auth

from httplib import HTTPConnection
from datetime import datetime

class Query:
    def __init__(self, host, func, **kwargs):
        params = '&'.join(['%s=%s' % item for item in kwargs.items() ])
        self.request = '/%s.aspx?%s' % (func, params)
        self.connection = HTTPConnection(host)
        self.response = None
        self.result = None
        self.status = 'init'
    def __str__(self):
        return str( {'status': self.status,
                     'request': self.request,
                     'response': self.response,
                     'result': self.result } )

    def _process_result(self):
        data = self.response
        if not data:
            return
        
        if data[0] == 'E':
            self.status = 'error'
            self.result = None
        elif data[0] == 'O':
            self.status = 'ok'

        result = []
        for line in data.split('\n')[1:]:
            if not line:
                continue
            
            if line[0] == 'H':
                params = line.split()
            else:
                params = line.split('\t')

            if len(params[0]) > 1:
                params.insert(0, 'D')

            if params[0] == 'H':
                keys = params[1:]
            elif params[0] == 'D':
                values = params[1:]
                if keys and (len(keys) == len(values)):
                    result.append(dict(zip(keys, values)))
            elif params[0] == '$':
                result.append({'$': params[1]})
                break
        self.result = result

    def execute(self):
        self.connection.request("GET", self.request)
        self.response = self.connection.getresponse().read()
        self._process_result()
        return self.result

class RPC:
    def __init__(self, pid=0, host=STELLA):
        self.host = host
        self.pid = pid

    def _make_auth(self, pid=None):
        return make_auth(pid or self.pid or 0)

    def make_query(self, func, **kwargs):
        apid = kwargs.get('authpid', self.pid)
        self.query = Query(self.host, func, **dict(kwargs, auth=self._make_auth(apid)))
        return self.query.execute()

    def getleaderboard(self, pos, after, type, **kwargs):
        return self.make_query('getleaderboard', pos=pos, after=after, type=type, **kwargs)

    def getplayerinfo(self, mode, pToken=None):
        return self.make_query('getplayerinfo', mode=mode)

    def getplayerprogress(self, mode, scale='game'):
        return self.make_query('getplayeprogress', mode=mode, scale=scale)

    def getunlocksinfo(self, pid):
        return self.make_query('getunlocksinfo', mode=mode, authpid=pid)

class StatsWrapper:
    def __init__(self, *args, **kwargs):
        self._rpc = RPC(*args, **kwargs)
        self.__init_modes()

    def _have_data(self, dic, fields):
        return len(dic.keys()) == len(filter( lambda f: f in dic, fields ))

    def _format(self, data, **format):
        return [
            dict([ ( key, fun(line[key]) )
                   for key, fun in format.items()])
            for line in data if self._have_data(line, format.keys())]

    def _timestamp(self, str):
        return datetime.fromtimestamp(int(str))

    def get_awards(self, pid):
        return self._format(
            self._rpc.make_query('getawardsinfo', pid=pid),
            first=int, when=self._timestamp, award=str, level=int)

    def get_backend_info(self):
        return self._format(
            make_query('getbackendinfo', authpid=0),
            config=str)
    
    def player_info(self, mode):
        modes = self.player_info_modes
        if mode not in modes:
            raise ValueError('Unknown mode: "%s"' % mode)
        return self._format(
            self._rpc.make_query('getplayerinfo', mode=mode),
            **modes[mode])

    def player_search(self, nick):
        return self._format(
            self._rpc.make_query('playersearch', nick=nick),
            nick=str, pid=int)

    def __init_modes(self):
        self.player_info_modes = {
        'ovr': {'acdt': self._timestamp, 'brs': int, 'crpt': int,
                'fe': int, 'fgm': int, 'fk': int, 'fm': int, 'fv': int, 'fw': int,
                'gsco': int, 'lgdt': self._timestamp, 'los': int, 'nick': str,
                'pdt': int, 'pdtc': int, 'pid': int, 'tid': int, 'tt': int,
                'win': int, 'etp-3': int},
        'ply':  {'adpr': float, 'akpr': float, 'dpm': float, 'dstrk': int, 'dths': int,
                 'kdr': float, 'kkls-0': int, 'kkls-1': int, 'kkls-2': int, 'kkls-3': int,
                 'klla': int, 'klls': int, 'klstrk': int, 'kpm': float, 'ktt-0': int,
                 'ktt-1': int, 'ktt-2': int, 'ktt-3': int, 'nick': str, 'ovaccu': float,
                 'pid': int, 'spm': float, 'suic': int, 'tid': int, 'toth': int, 'tots': int},
        }

