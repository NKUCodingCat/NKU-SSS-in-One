#include <cstdlib>
#include <string>
using namespace std;
int main(int argc, char *argv[]) {
    string p(argv[0]), path;
    bool record = false;
    for (int i = p.length() - 1; i >= 0; i--) {
        if (p[i] == '/') record = true;
        if (record) path = p[i] + path;
    }
    string cmd = "python " + path + "prog/Launcher.py";
    system(cmd.c_str());
    return 0;
}

