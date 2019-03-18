#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <regex>

using namespace std;

int getInvCount(const vector<int> & arr)
{
	int inv_count = 0;
	for (int i = 0; i < arr.size(); i++)
		for (int j = i + 1; j < arr.size(); j++)
			if (arr[j] && arr[i] && arr[i] > arr[j])
				inv_count++;
	return inv_count;
}

bool isSolvable(const vector<int> & arr)
{
	int invCount = getInvCount(arr);

	return (invCount % 2 == 0);
}



const vector<int> fileReader(const string & fileName)
{
	ifstream inFile;

	inFile.open(fileName);
	if (!inFile)
	{
		cerr << "Unable to open file " + fileName;
		exit(1);
	}
	string line;


	while(getline(inFile, line))
	{
		std::cmatch res;
		while (regex_match(line.c_str(), res, std::regex("(.*)#(.*)")))
			line.erase((unsigned long)res[1].length(), line.length());
		
	}
	inFile.close();
}

int main(int argc, char **argv)
{

	return (0);
}