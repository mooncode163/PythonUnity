
# HomeBrew
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/sbin:$PATH"
# HomeBrew END


# Java


JAVA_HOME=/Applications/Android\ Studio.app/Contents/jre/jdk/Contents/Home
PATH=$PATH:$JAVA_HOME/bin
PATH=$JAVA_HOME/bin:$PATH:.
CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:
export JAVA_HOME
export PATH
export CLASSPATH

# Java END

#dotnet 
export PATH="/usr/local/share/dotnet:$PATH"
#dotnet end

#mono 
export PATH=/Library/Frameworks/Mono.framework/Versions/Current/bin:${PATH}
#mono end


#adb 
export PATH="/Users/moon/Library/Android/sdk/platform-tools:$PATH"
#adb end

#adb 
export PATH="/Users/moon/sourcecode:$PATH"
#adb end

export PATH=${PATH}:/usr/local/mysql/bin


# gradle
export PATH=${PATH}:/Users/moon/sourcecode/unity/product/Common/Tool/gradle/gradle-4.10.1/bin






