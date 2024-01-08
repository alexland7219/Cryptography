#include <cryptopp/cryptlib.h>
#include <cryptopp/base64.h>
#include <cryptopp/hex.h>
#include <cryptopp/rsa.h>
#include <cryptopp/files.h>
#include <cryptopp/pssr.h>
#include <cryptopp/sha.h>
#include <iostream>
#include <thread>
#include <omp.h>
#include <vector>
using namespace CryptoPP;

const std::string b64signature ="iZtBXT2jxLDuQZpTeO3qJx9EtQvhfgsIz+O9TZ6W3KvV610pTmZib+8vLdamTP7GCwKj8/0vqfG9SfWHmU4T62gYbS2FuWC/iqeIWhTMkpixpYK099PE4PZibSlz5gdb9YJDrPphXdaMccpESCs1zyffIfj/oUgdD0zWl57T0JqnlkLATmiwwHnvX88Kzs86f15TT4iX5how0KVQ5d0sUD2PgvOfuZZ3WcMndGiuyf9WCtlKc4nvhtqO8tGOknt1fzaHt6i4Id9qibq6M6TBbkmzcO93EabJnOV7si69oT41zTjKZ+vJ9yTQW/eVWd6NMUZ3DhPJ5OHO4LWQQ==";

const std::string message = "FyYV+4C63IdusbJd/ve1VyRGN8EkemqIaD9LvxjqIqc=;40289dc5869377b20188bea120e34006;40289dc4869376800188be0caab75ad0;1687337327495";


void procesVerification( char a, char b, char c , char d, char e, RSASS<PSS, SHA256>::Verifier& verifier)
{
	std::string B64signature = std::string(1, a) + std::string(1, b) + std::string(1, c) + std::string(1, d) + std::string(1, e) + b64signature; 
	std::string sig;

    StringSource ss(B64signature, true, new Base64Decoder(new StringSink(sig)));

	bool result = verifier.VerifyMessage(
		(const byte*)message.data(), message.size(),
		(const byte*)sig.data(), sig.size());

	if (result)
	{
		std::cout << "FOUND THE STRING: " + std::string(1, a) + std::string(1, b) + std::string(1, c) + std::string(1, d) + std::string(1, e) << std::endl;
		exit(0);
	}
}

int main(int, char **)
{
    const std::string base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	Integer N("0xa1fee0ba40faf8ab1352af26407fa61706bd91dc5c01e6606c29101ae15efa986c66ea80456f3d463ee9dc37846e5b21bbddb853a05c93dc957fddc67df0392df0beee0aeea73a7087c9ca18faac1dce10044d6b2b48b435cd87937bb52fff1e4f349073febf75c980dc3def31d84ada923d9c3219d93d73d3c70f77cef4273daed4fab0632ab447482379019158823dc923cedfbc4930f6aa8f4adbfe0db3bfc80967642d4bb7c17126cdaf901cd262e912febc7ccd0f98030709dab1c02b5b17c9e74c7d1402e7fdb43b9ead1a02c66294098a2de5d4a1517c20d46c23234f87b746d54b4ed0eca1c4a3762b588e89675f632b5f6e91420f47ce05f24870a9");
	Integer e("65537");

	RSA::PublicKey server_pk;
	server_pk.Initialize(N, e);

	// Verifier
	RSASS<PSS, SHA256>::Verifier verifier(server_pk);

	std::vector<std::thread> threads;

	for (char a : base64Chars)
		for (char b : base64Chars)
			for (char c : base64Chars)
				for (char d : base64Chars)
					#pragma omp parallel for
					for (char e : base64Chars)
					{
						// std::cout << a << b << c << d << e << std::endl;
						procesVerification(a, b, c, d, e, verifier);
						//threads.emplace_back(procesVerification, a, b, c, verifier);
					}

	return 0;
}
