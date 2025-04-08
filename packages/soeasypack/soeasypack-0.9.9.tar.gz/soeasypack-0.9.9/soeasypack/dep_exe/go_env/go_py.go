/*
 * @Author: xmqsvip
 * @Date: 2024-12-07
 * @LastEditTime: 2024-12-22 17:13:29
 */

package main

import (
	"os"
	"syscall"
	"unsafe"
)

func MessageBox(title, message string) {
	msgBox := syscall.MustLoadDLL("user32.dll")
	defer msgBox.Release()
	proc := msgBox.MustFindProc("MessageBoxW")

	// 处理 UTF16PtrFromString 的返回值
	titlePtr, _ := syscall.UTF16PtrFromString(title)
	messagePtr, _ := syscall.UTF16PtrFromString(message)

	proc.Call(
		0,
		uintptr(unsafe.Pointer(messagePtr)),
		uintptr(unsafe.Pointer(titlePtr)),
		0,
	)
}

func fileExists(filename string) bool {
	_, err := os.Stat(filename)
	if err != nil {
		if os.IsNotExist(err) {
			return false
		}
		return false
	}
	return true
}

func main() {
	var pyDllPath string
	var mainFile string
	pythonHome := os.Getenv("PYTHONHOME")
	if pythonHome == "" {
		// 获取当前目录并设置 PYTHONHOME
		currentDir, _ := os.Getwd()
		os.Setenv("PYTHONHOME", currentDir+"\\rundep")
		pyDllPath = currentDir + "\\rundep\\python3.dll"
		os.Setenv("pyDllPath", pyDllPath)
		// 切换工作目录
		os.Chdir(currentDir + "\\rundep\\AppData")
		//获取程序主入口文件
		mianFiles := []string{"main.pyc", "main.py", "main.pyw"}
		for _, file := range mianFiles {
			if fileExists(file) {
				mainFile = file
				os.Setenv("mainFile", mainFile)
				break
			}
		}
		if mainFile == "" {
			MessageBox("错误", pythonHome+"\\AppData,找不到 main.pyc(.py.pyw)文件")
			os.Exit(1)
		}
	} else {
		pyDllPath = os.Getenv("pyDllPath")
		mainFile = os.Getenv("mainFile")
	}

	// 加载 python3.dll
	pythonDll, err := syscall.LoadDLL(pyDllPath)
	if err != nil {
		MessageBox("错误", "无法加载 python3.dll: "+err.Error())
		return
	}
	defer pythonDll.Release()

	// 获取 Py_Main 函数的地址
	pyMainProc, err := pythonDll.FindProc("Py_Main")
	if err != nil {
		MessageBox("错误", "无法找到 Py_Main 函数: "+err.Error())
		return
	}

	args := []string{"python", mainFile}
	args = append(args, os.Args[1:]...)

	// 将命令行参数转换为 C 字符串
	var cArgs []uintptr
	for _, arg := range args {
		arg_, _ := syscall.UTF16PtrFromString(arg)
		cArgs = append(cArgs, uintptr(unsafe.Pointer(arg_)))
	}

	// 调用 Py_Main 函数执行 Python 脚本
	argc := len(args)
	argv := uintptr(unsafe.Pointer(&cArgs[0]))
	ret, _, _ := pyMainProc.Call(uintptr(argc), argv)
	if ret != 0 {
		MessageBox("错误", "执行失败,cmd运行run.bat查看报错信息")
	}

	finalize, _ := pythonDll.FindProc("Py_Finalize")
	finalize.Call()
}
