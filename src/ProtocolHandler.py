class ProtocolHandler:
    def __call__(self, player, protocol):
        protocol_name = protocol['protocol']
        if not hasattr(self, protocol_name):
            return None
        # 调用与协议同名的方法
        method = getattr(self, protocol_name)
        result = method(player, protocol)
        return result

    @staticmethod
    def cli_login(player, protocol):
        """
        客户端登录请求
        """
        # 数据存储单元
        data = [
            ['admin01', '123456', '玩家昵称1'],
            ['admin02', '123456', '玩家昵称2'],
            ['admin03', '123456', '玩家昵称3'],
        ]
        username = protocol.get('username')
        password = protocol.get('password')

        # 校验帐号密码是否正确
        login_state = False
        nickname = None
        for user_info in data:
            if user_info[0] == username and user_info[1] == password:
                login_state = True
                nickname = user_info[2]
                break

        # 登录不成功
        if not login_state:
            player.send({"protocol": "ser_login", "result": False, "msg": "账号或密码错误"})
            return

        # 登录成功
        player.login_state = True
        player.game_data = {
            'uuid': uuid.uuid4().hex,
            'nickname': nickname,
            'x': 5,  # 初始位置
            'y': 5
        }

        # 发送登录成功协议
        player.send({"protocol": "ser_login", "result": True, "player_data": player.game_data})

        # 发送上线信息给其他玩家
        player.send_without_self({"protocol": "ser_online", "player_data": player.game_data})

        player_list = []
        for p in player.connections:
            if p is not player and p.login_state:
                player_list.append(p.game_data)
        # 发送当前在线玩家列表（不包括自己）
        player.send({"protocol": "ser_player_list", "player_list": player_list})
