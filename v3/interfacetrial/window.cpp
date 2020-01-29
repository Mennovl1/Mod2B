// Include GLFW
#include <cstdio>
#include <GL/glew.h>
#include <GLFW/glfw3.h>

void render(){
    // Clear the screen
    // glClearColor(0.0, 0.0, 0.4, 1.0);
    glClear( GL_COLOR_BUFFER_BIT );
    glLoadIdentity();//load identity matrix
    
    glTranslatef(0.0f,0.0f,-4.0f);//move forward 4 units

    glPointSize(100.0f); // 10px
    glColor3f(0.0f,0.0f,1.0f); //blue color

    glBegin(GL_POINTS);
    glVertex3f(0.0f,0.0f,0.0f);//upper-right corner
    glVertex3f(-1.0f,-1.0f,0.0f);//lower-left corner
    glEnd();
    glClear( GL_COLOR_BUFFER_BIT );
    // fprintf(stderr, "frame\n");
}

int main(){
    // Initialise GLFW
    // bool glewExperimental = false; // Needed for core profile
    if( !glfwInit() ){
        fprintf( stderr, "Failed to initialize GLFW\n" );
        return -1;
    };

    glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // We want OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We don't want the old OpenGL 

    // // Open a window and create its OpenGL context
    GLFWwindow* window; // (In the accompanying source code, this variable is global for simplicity)
    window = glfwCreateWindow( 1024, 768, "Universe", NULL, NULL);
    if( window == NULL ){
        fprintf( stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n" );
        glfwTerminate();
        return -1;
    };
    glfwMakeContextCurrent(window); // Initialize GLEW
    glewExperimental=true; // Needed in core profile
    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        return -1;
    }
    
    // Ensure we can capture the escape key being pressed below
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

    do{
    
        render();
        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

    } // Check if the ESC key was pressed or the window was closed
    while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
        glfwWindowShouldClose(window) == 0 );
    return 1;
};

