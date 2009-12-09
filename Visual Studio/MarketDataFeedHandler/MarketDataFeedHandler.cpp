#include "quickfix/FileStore.h"
#include "quickfix/FileLog.h"
#include "quickfix/SocketInitiator.h"

#include <stdio.h>
#include <iostream>

#include "Application.h"

int main( int argc, char** argv )
{
	try
	{
		std::string fileName = "C:\\quickfix\\bin\\cfg\\MarketDataFeedHandler.cfg";
		FIX::SessionSettings settings(fileName);

		Application application;
		FIX::FileStoreFactory storeFactory(settings);
		FIX::FileLogFactory logFactory(settings);
		FIX::SocketInitiator initiator(application, storeFactory, settings, logFactory);

		initiator.start();
		std::cout << "Press enter to stop the feed." << std::endl;
		getchar();		
		initiator.stop();
	}
	catch(FIX::ConfigError& e)
	{
		std::cout << e.what();
		return 1;
	}

	std::cout << "Press enter to exit." << std::endl;
	getchar();

	return 0;
}
