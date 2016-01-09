/*
	Attention: I use gcc 4.5.2 in Haskell to compile
	NKUCodingCat Jan 7，2016
*/

#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <libgen.h> 
#include <unistd.h> /* for fork */
#include <windows.h>
#include <string.h>

#define BINARY   "prog\\python27.exe"
#define LAUNCHER "prog\\Launcher.py"

int main()
{
    /*Spawn a child to run the program.*/
	fprintf(stdout, "\
================================================================================\r\n\
\r\n    NKU-SSS-in-One Program General Launcher on Windows Powered by MinGW\r\n\r\n\
    Mail to nankai.codingcat@outlook.com if any question\r\n\
\r\n                             ----- NKUCodingCat & Neon4o4      \r\n\
\r\n\r\n    Come and Join us :  Everything-in-NKU on Github.com \r\n\
================================================================================\r\n\
	");
	char cwd[1024];
	if (GetModuleFileName(NULL, cwd, sizeof(cwd)) != 0){
		// ====Create New Process====
		
		char Command[2048];
		sprintf(Command, "%s %s", BINARY, LAUNCHER);
		
		STARTUPINFO si;
		PROCESS_INFORMATION pi;
	
		ZeroMemory( &si, sizeof(si) );
		si.cb = sizeof(si);
		ZeroMemory( &pi, sizeof(pi) );
		
		// Start the child process. 
		if( !CreateProcess( NULL,
			Command,        
			NULL,           
			NULL,           
			FALSE,          
			0,              
			NULL,           
			dirname(cwd),   
			&si,            
			&pi )           
		) 
		{
			printf( "CreateProcess failed (%d).\n", GetLastError() );
		}
		
		// Wait until child process exits.
		WaitForSingleObject( pi.hProcess, INFINITE );
		
		// Close process and thread handles. 
		CloseHandle( pi.hProcess );
		CloseHandle( pi.hThread );
		
	}
		// ====      END         =====
	else
		{perror("getcwd() error");}
	system("PAUSE");
	return 0;
	
}