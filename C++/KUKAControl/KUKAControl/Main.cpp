/*

reference
http://blog.livedoor.jp/akf0/archives/51585502.html //ソケット通信
http://www.geocities.jp/eneces_jupiter_jp/cpp1/010-055.html //文字列置換
*/

#include <iostream>
#include <string>
#include <tchar.h>
#include <WinSock2.h>
#include <Ws2tcpip.h> //inet_pton()

#pragma comment(lib, "WSock32.lib")
#pragma comment(lib, "ws2_32.lib")


std::string replace(std::string String1, std::string String2, std::string String3)
{
	std::string::size_type Pos(String1.find(String2));

	while (Pos != std::string::npos)
	{
		String1.replace(Pos, String2.length(), String3);
		Pos = String1.find(String2, Pos + String3.length());
	}

	return String1;
}


std::string generateMoveJSON(float lx, float ly,float lz, float ax, float ay, float az){

	std::string json = R"(	
		{
			"op": "publish",
			"topic": "/cmd_vel", 
			"msg": {
				"linear": {"x": %lx%, "y": %ly%, "z": %lz%}, 
				"angular": {"x": %ax%, "y": %ay%, "z": %az%}
			}
		}
	)";

	json = replace(json, "%lx%", std::to_string(lx));
	json = replace(json, "%ly%", std::to_string(ly));
	json = replace(json, "%lz%", std::to_string(lz));
	json = replace(json, "%ax%", std::to_string(ax));
	json = replace(json, "%ay%", std::to_string(ay));
	json = replace(json, "%az%", std::to_string(az));

	return json;
}

//=======================================================================================

int main(void){
 
	const char host[] = "192.168.100.40";
	const int port = 9090;
	const float vel = 0.2f;

	SOCKET sock;
	struct sockaddr_in dest;

	//準備
	WSADATA data;
	WSAStartup(MAKEWORD(2, 0), &data);
	memset(&dest, 0, sizeof(dest));
	dest.sin_port = htons(port);
	dest.sin_family = AF_INET;
	inet_pton(AF_INET, host, &dest.sin_addr);
	sock = socket(AF_INET, SOCK_STREAM, 0);

	//サーバへの接続
	if (connect(sock, (struct sockaddr *) &dest, sizeof(dest))){
		std::cout << "failed connection" << std::endl;
		exit(-1);
	}
	else {
		std::cout << "success connection" << std::endl;
	}

	//制御ループ
	std::cout << "press key [wsad] to move youbot" << std::endl;
	float lx, ly, lz, ax, ay, az;
	lx = 0.0f;
	while (true) {
		lx = 0.0f; ly = 0.0f; lz = 0.0f; ax = 0.0f; ay = 0.0f; az = 0.0f;
		
		std::string key;
		std::cin >> key;
		if (key[0] == 'w')
			lx = vel;
		else if (key[0] == 's')
			lx = -vel;
		else if (key[0] == 'a')
			az = vel;
		else if (key[0] == 'd')
			az = -vel;
		else if (key[0] == 'q')
			break;

		//JSONを生成して, charに変換してから送信
		std::string json = generateMoveJSON(lx,ly,lz, ax,ay,az);
		char* buf = (char*)json.c_str();
		send(sock, buf, sizeof(buf), 0);
	}

	//移動停止
	std::string json = generateMoveJSON(0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f);
	char* buf = (char*)json.c_str();
	send(sock, buf, sizeof(buf), 0);

	closesocket(sock);
	WSACleanup();

	return 0;

}