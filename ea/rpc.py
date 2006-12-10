# -*- coding: utf-8 -*-

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

    def getplayerprogress(self, mode, scale='game'):
        return self.make_query('getplayeprogress', mode=mode, scale=scale)

class StatsWrapper:
    def __init__(self, *args, **kwargs):
        self._rpc = RPC(*args, **kwargs)
        self.__init_modes()

    def _have_data(self, dic, fields, fuzzy=False):
        found = len(filter( lambda f: f in dic, fields ))
        return (not fuzzy and found == len(fields)) or (fuzzy and found)

    def _format(self, data, fuzzy=False, **format):
        return [
            dict([ ( key, fun(fuzzy and line.get(key, '000') or line[key] ))
                   for key, fun in format.items()])
            for line in data
            if self._have_data(line, format.keys()) or fuzzy
            ]

    def _timestamp(self, str):
        return datetime.fromtimestamp(int(str))

    def get_awards(self, pid=0):
        """ Gets a list of awards for a particular player.
        """
        return self._format(
            self._rpc.make_query('getawardsinfo', pid=pid or self._rpc.pid),
            first=self._timestamp, when=self._timestamp, award=str, level=int)

    def get_backend_info(self):
        """ Gets information used to update various files for the game.
        At the moment it returns some pythonic code for the config file
        used to determine awards and rank criteria.
        """
        return self._format(
            make_query('getbackendinfo', authpid=0),
            config=str)
    
    def player_info(self, mode):
        """ Gets player information.
        mode (required) - the stats mode that takes one of the following parameters:

            base (requires pToken) - general statistics
            ovr - overview stats
            ply - player stats
            titan - titan mode stats
            wrk - teamwork stats
            com - leadership stats
            wep - weapon stats
            veh - vehicle stats
            map - map stats
        """
        modes = self.player_info_modes
        if mode not in modes:
            raise ValueError('Unknown mode: "%s"' % mode)
        data = self._rpc.make_query('getplayerinfo', mode=mode)
        if mode in ('wep', 'veh', 'map'): #those could not contain all the rows. thank you dice/ea!
            if type(modes[mode]) is list:
                # multiple line formats
                results = reduce( lambda x,y:x+y,
                                  [ self._format( data, fuzzy=True, **format )
                                    for format in modes[mode] ] )
            else:
                results = self._format( data, fuzzy=True, **modes[mode])
            return [result for result in results # drop empty rows after fuzzy formatting
                    if sum(map(int, filter(lambda x: x != '000', result.values())))]
        else:
            return self._format( data, **modes[mode])

    def get_leader_board(self, pos, after, mode, **kwargs):
        """ Gets the BF2142 leaderboard information
        mode (required) - the general category in which to get the results. valid values for this are:
            weapon (requires id) - ranks players by weapon.
                                   there are 43 some odd different types of weapons.
                                   setting the id parameter to a value between 0 - 27
                                   (though more may possibly be pulled... that hasn't been tested)
                                   will return a result for that weapon. not all weapons kill.
            vehicle (requires id) - rank players based on a particular vehicle. the id parameter takes values 0 - 14
            overallscore - rank players based on overall score
            combatscore - rank players based on combat score
            commanderscore - rank players on commander score
            teamworkscore - rank players based on teamwork score
            efficiency - rank players based on efficiency
            risingstar - rank players based on the player who has progressed the most over some period of time?
            supremecommander - shows "hall of fame" board and will display whoever has achieved the "supreme commander" rank
        id (required by vehicle & weapon) - specifies a weapon or vehicle type.
        ccFilter (optional) - filters result set by country (takes the 2 letter country code as its value)
        buddiesFilter (optional) - filters results based on a list of buddy PID's.
                                   ex: buddiesFilter=(81168298, 81242994, 81306093, 81465904)
        dogTagFilter (optional) - filters the list to people you've knifed (set dogTagFilter=1 to enable this filter).
        """
        modes = self.leader_board_modes
        if mode not in modes:
            raise ValueError('Unknown mode: "%s"' % mode)
        if mode in ('weapon', 'vehicle') and 'id' not in kwargs:
            raise ValueError('"id" argument is required for mode "%s"' % mode)
        return self._format(
            self._rpc.make_query('getleaderboard', pos=pos, after=after, type=mode, **kwargs),
            **modes[mode])

    def get_player_progress(self, mode, scale='game'):
        """ Gets statistical progress data used to draw the graphs in game
        """
        modes = self.player_progress_modes
        if mode not in modes:
            raise ValueError('Unknown mode: "%s"' % mode)
        return self._format(
            self._rpc.make_query('getleaderboard', mode=mode, scale=scale)
            **modes[mode])

    def get_unlocks_info(self, pid=0):
        """ Gets a list of unlocked items.

        first digit: Kit
        second digit: Col of unlock tree 1 or 2
        third digit: Order in unlock tree 1 to 4(highest)
        """
        return self._format(
            self._rpc.make_query('getunlocksinfo', authpid=pid or self._rpc.pid),
            UnlockID=str)

    def player_search(self, nick):
        """ Finds a players based on their nick.
        Use '*' as wildcard.
        """
        return self._format(
            self._rpc.make_query('playersearch', nick=nick),
            nick=str, pid=int)

    def __init_modes(self):
        """ Precompile format dicts
        because they are different for each mode, containg '-'ses and not normalised.
        """
        # those should be grabbed directly from the game
        WEAPONS = 43
        VEHICLES = 15
        MAPS = 9
        MAP_MODES = 2
        
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
        'titan':{'cts': int, 'nick': str, 'pid': int, 'tas': int, 'tcd': int, 'tcrd': int,
                 'tdrps': int, 'tds': int, 'tgd': int, 'tgr': int, 'tid': int, 'trp': int,
                 'ttp': int},
        'wrk':  {'capa': int, 'cpt': int, 'cs': int, 'cts': int, 'dass': int, 'dcpt': int,
                 'hls': int, 'nick': str, 'pid': int, 'resp': int, 'rps': int, 'rvs': int,
                 'sasl': int, 'tac': int, 'talw': int, 'tasl': int, 'tasm': int, 'tdmg': int,
                 'tid': int, 'tkls': int, 'tvdmg': int, 'twsc': int},
        'com':  {'cs': int, 'csgpm-0': int, 'csgpm-1': int, 'kluav': int, 'nick': str,
                 'pid': int, 'sasl': int, 'slbcn': int, 'slbspn': int, 'slpts': int,
                 'sluav': int, 'tac': int, 'tasl': int, 'tid': int, 'wkls-27': int},
        'wep': dict( # generate what awfull number of rows
                     reduce(lambda x,y: x+y,
                            [ [('%s-%d' % (key, n), val) for n in range(WEAPONS)]
                              for key, val in
                              { 'waccu': float, 'wdths': int, 'whts':int, 'wkdr':float,
                                'wkls':int, 'wshts':int, 'wtp': int, 'wtpk': int,
                              }.items()])),
        'veh': dict( # generate what not-so-awfull-but-still-more-than-one number of rows
                     reduce(lambda x,y: x+y,
                            [ [('%s-%d' % (key, n), val) for n in range(VEHICLES)]
                              for key, val in
                              { 'vdstry': float, 'vdths': int, 'vkdr': float, 'vkls': int,
                                'vrkls': int, 'vtp': int,
                              }.items()])),
        'map': [dict( # boring...
                     reduce(lambda x,y: x+y,
                            [ [('%s-%d-%d' % (key, mode, n), val) for n in range(MAPS)]
                              for key, val in
                              { 'mbr': int, 'mlos': int, 'msc': int, 'mtt': int, 'mwin': int,
                              }.items()]))
                for mode in range(MAP_MODES)],
        }

        base = { 'Vet': int, 'countrycode': str, 'nick': str, 'pid': int,
                       'pos': int, 'rank': int, 'playerrank': int} # 'dt': int
        self.leader_board_modes = {
            'overallscore':   dict(base, globalscore=int),
            'combatscore':    dict(base, Accuracy=float, Deaths=int, Kills=int, kdr=float),
            'risingstar':     dict(base, PercentChange=float),
            'commanderscore': dict(base, coscore=int),
            'teamworkscore':  dict(base, teamworkscore=int),
            'efficiency':     dict(base, Efficiency=float),

            'weapon':         dict(base, accuracy=float, deaths=int, kdr=float, kills=int),
            'vehicle':        dict(base, roadkills=int,  deaths=int, kills=int),

            'supremecommander': {'Date': self._timestamp, 'Times': int, 'Week': int,
                                 'nick': str, 'rank': int, 'Vet': lambda x:x in ('True', 1, '1', True)},
        }

        self.player_progress_modes = {
            'point': {},
            'score': {},
            'ttp': {},
            'kills': {},
            'spm': {},
            'role': {},
            'flag': {},
            'waccu': {},
            'wl': {},
            'twsc': {},
            'sup': {},
        }
