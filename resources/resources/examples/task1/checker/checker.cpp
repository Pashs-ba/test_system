#include "testlib.h"
#include <iostream>
using namespace std;

int main(int argc, char* argv[])
{
   /// std::fprintf(stderr, "%s", "\n\n---sas---\n\n");

    ///char c1[] = "C:\\Users\\fedorovas\\source\\repos\\ConsoleApplication7\\ConsoleApplication7\\resources\\ans.txt";
    ///char c2[] = "C:\\Users\\fedorovas\\source\\repos\\ConsoleApplication7\\ConsoleApplication7\\resources\\output.txt";
    ///char c3[] = "C:\\Users\\fedorovas\\source\\repos\\ConsoleApplication7\\ConsoleApplication7\\resources\\answer.txt";
    ///char c4[] = "C:\\Users\\fedorovas\\source\\repos\\ConsoleApplication7\\ConsoleApplication7\\resources\\rr.txt";

    ///char* ss[] = { 0, c1,c2,c3 };

    setName("compares two signed integers");
   // registerTestlibCmd(4, ss);
    registerTestlibCmd(argc, argv);
    int ja = ans.readInt();
    int pa = ouf.readInt();
   
    if (ja != pa)
        quitf(_wa, "expected %d, found %d", ja, pa);
    quitf(_ok, "answer is %d", ja);
}


/*

registerTestlibCmd(int argc, char *argv[]) {

    inf.init(argv[1], _input);
    ouf.init(argv[2], _output);
    ans.init(argv[3], _answer);



void InStream::quitscr(WORD color, const char *msg) {
    if (resultName == "") {
        textColor(color);
        std::fprintf(stderr, "%s", msg);
        textColor(LightGray);
    }
}



NORETURN void quit(TResult result, const std::string &msg) {
    ouf.quit(result, msg.c_str());
}


    InStream ouf;
*/
