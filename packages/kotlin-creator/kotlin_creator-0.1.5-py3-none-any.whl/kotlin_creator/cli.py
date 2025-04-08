import click
import os
import shutil
import subprocess
from pathlib import Path
import sys

def create_kotlin_project_structure(project_name):
    """Create a comprehensive Kotlin Clean Architecture project structure"""
    base_path = Path(project_name)
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Root files
    (base_path / "CleanArchitectureExample.zip").touch()
    (base_path / "gradle.properties").touch()
    (base_path / "gradlew").touch()
    (base_path / "gradlew.bat").touch()
    (base_path / "build.gradle").touch()
    (base_path / "settings.gradle").touch()

    # Create the app module
    app_path = base_path / "app"
    app_path.mkdir(parents=True, exist_ok=True)
    (app_path / "proguard-rules.pro").touch()
    (app_path / ".gitignore").touch()
    (app_path / "build.gradle").touch()
    
    # Create the core module
    core_path = base_path / "core"
    core_path.mkdir(parents=True, exist_ok=True)
    (core_path / "consumer-rules.pro").touch()
    (core_path / "proguard-rules.pro").touch()
    (core_path / ".gitignore").touch()
    (core_path / "build.gradle").touch()
    
    # Create gradle wrapper directory
    gradle_wrapper_path = base_path / "gradle" / "wrapper"
    gradle_wrapper_path.mkdir(parents=True, exist_ok=True)
    (gradle_wrapper_path / "gradle-wrapper.properties").touch()
    
    # Create app module structure
    app_src_main_path = app_path / "src" / "main"
    app_src_main_path.mkdir(parents=True, exist_ok=True)
    (app_src_main_path / "AndroidManifest.xml").touch()
    
    # App module Java paths
    app_java_path = app_src_main_path / "java" / "com" / "hazelmobile" / "cleanarchitecture"
    app_java_path.mkdir(parents=True, exist_ok=True)
    
    # Create app test directories
    app_test_path = app_path / "src" / "test" / "java" / "com" / "hazelmobile" / "cleanarchitecture"
    app_test_path.mkdir(parents=True, exist_ok=True)
    (app_test_path / "ExampleUnitTest.kt").touch()
    
    # Create app androidTest directories
    app_android_test_path = app_path / "src" / "androidTest" / "java" / "com" / "hazelmobile" / "cleanarchitecture"
    app_android_test_path.mkdir(parents=True, exist_ok=True)
    (app_android_test_path / "ExampleInstrumentedTest.kt").touch()
    
    # Create app resource directories and files
    res_path = app_src_main_path / "res"
    
    # Create various resource directories
    resource_dirs = [
        "anim", "drawable", "drawable-v24", "layout", "mipmap-anydpi-v26", 
        "mipmap-hdpi", "mipmap-mdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi",
        "navigation", "values", "values-land", "values-night", "values-v23", 
        "values-w1240dp", "values-w600dp"
    ]
    
    for dir_name in resource_dirs:
        (res_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Create animation XML files
    (res_path / "anim" / "slide_in_bottom.xml").touch()
    (res_path / "anim" / "slide_out_bottom.xml").touch()
    
    # Create drawable XML files
    (res_path / "drawable" / "dialog_background.xml").touch()
    (res_path / "drawable" / "ic_launcher_background.xml").touch()
    (res_path / "drawable-v24" / "ic_launcher_foreground.xml").touch()
    
    # Create layout XML files
    layout_files = [
        "activity_company_listing.xml", "activity_company_multi_view.xml", 
        "fragment_common_dialogue.xml", "item_ad.xml", "item_company.xml", "item_date.xml"
    ]
    for layout_file in layout_files:
        (res_path / "layout" / layout_file).touch()
    
    # Create mipmap files
    (res_path / "mipmap-anydpi-v26" / "ic_launcher.xml").touch()
    (res_path / "mipmap-anydpi-v26" / "ic_launcher_round.xml").touch()
    
    for mipmap_dir in ["mipmap-hdpi", "mipmap-mdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi"]:
        (res_path / mipmap_dir / "ic_launcher.webp").touch()
        (res_path / mipmap_dir / "ic_launcher_round.webp").touch()
    
    # Create navigation file
    (res_path / "navigation" / "nav_graph.xml").touch()
    
    # Create values files
    values_files = {
        "values": ["colors.xml", "dimens.xml", "strings.xml", "themes.xml"],
        "values-land": ["dimens.xml"],
        "values-night": ["themes.xml"],
        "values-v23": ["themes.xml"],
        "values-w1240dp": ["dimens.xml"],
        "values-w600dp": ["dimens.xml"]
    }
    
    for dir_name, files in values_files.items():
        for file_name in files:
            (res_path / dir_name / file_name).touch()
    
    # Create app Java files and directories
    (app_java_path / "StockApplication.kt").touch()
    
    # Create data directory structure
    data_dir = app_java_path / "data"
    data_subdirs = [
        "csv", "local/datasources", "local/db", "mapper", 
        "remote/datasources", "remote/network/dto", "repositories"
    ]
    for subdir in data_subdirs:
        (data_dir / Path(subdir)).mkdir(parents=True, exist_ok=True)
    
    # Create data layer files
    data_files = {
        "csv": ["CSVParser.kt", "CompanyListingsParser.kt"],
        "local/datasources": ["LocalDataSource.kt", "LocalDataSourceImpl.kt"],
        "local/db": ["CompanyListingEntity.kt", "StockDao.kt", "StockDatabase.kt"],
        "mapper": ["CompanyListingMapper.kt", "Mapper.kt"],
        "remote/datasources": ["RemoteDataSource.kt", "RemoteDataSourceImpl.kt"],
        "remote/network": ["StockApi.kt"],
        "remote/network/dto": ["CompanyInfoDto.kt", "IntradayInfoDto.kt"],
        "repositories": ["StockRepository.kt", "StockRepositoryImplWithDataSource.kt"]
    }
    
    for subdir, files in data_files.items():
        for file_name in files:
            (data_dir / Path(subdir) / file_name).touch()
    
    # Create di (dependency injection) directory
    di_dir = app_java_path / "di"
    di_dir.mkdir(parents=True, exist_ok=True)
    di_files = ["AppModule.kt", "FilterManagerModule.kt", "MapperModule.kt", "RepositoryModule.kt", "UseCaseModule.kt"]
    for file_name in di_files:
        (di_dir / file_name).touch()
    
    # Create domain directory
    domain_dir = app_java_path / "domain"
    (domain_dir / "model").mkdir(parents=True, exist_ok=True)
    (domain_dir / "usecase").mkdir(parents=True, exist_ok=True)
    
    # Domain model files
    model_files = ["CompanyInfo.kt", "CompanyListing.kt", "IntradayInfo.kt"]
    for file_name in model_files:
        (domain_dir / "model" / file_name).touch()
    
    # Domain usecase files
    usecase_files = ["GetCompanyListingUseCase.kt", "GetCompanyListingsUseCase.kt"]
    for file_name in usecase_files:
        (domain_dir / "usecase" / file_name).touch()
    
    # Create UI directory
    ui_dir = app_java_path / "ui"
    ui_subdirs = ["common", "dashboard_company_listing/adapters", "multitype"]
    for subdir in ui_subdirs:
        (ui_dir / Path(subdir)).mkdir(parents=True, exist_ok=True)
    
    # UI files
    ui_files = {
        "common": ["CommonDialogueEvent.kt", "CommonDialogueFragment.kt", "CommonDialogueState.kt", "CommonDialogueViewModel.kt"],
        "dashboard_company_listing": ["CompanyListingActivity.kt", "CompanyListingsEvent.kt", "CompanyListingsState.kt", "CompanyListingsViewModel.kt"],
        "dashboard_company_listing/adapters": ["CompanyAdapter.kt", "CompanyAdapterMultiSelection.kt", "CompanyFilterStrategy.kt"],
        "multitype": ["CompanyAdapterMultiViews.kt", "CompanyMultiTypeActions.kt", "CompanyMultiViewActivity.kt", "CompanyMultipleViewModel.kt", "MultiTypeModel.kt"]
    }
    
    for subdir, files in ui_files.items():
        for file_name in files:
            (ui_dir / Path(subdir) / file_name).touch()
    
    # Create core module structure
    core_src_main_path = core_path / "src" / "main"
    core_src_main_path.mkdir(parents=True, exist_ok=True)
    (core_src_main_path / "AndroidManifest.xml").touch()
    
    # Core Java path
    core_java_path = core_src_main_path / "java" / "com" / "hazelmobile" / "cores"
    core_java_path.mkdir(parents=True, exist_ok=True)
    
    # Create core test directories
    core_test_path = core_path / "src" / "test" / "java" / "com" / "hazelmobile" / "cores"
    core_test_path.mkdir(parents=True, exist_ok=True)
    (core_test_path / "ExampleUnitTest.kt").touch()
    
    # Create core androidTest directories
    core_android_test_path = core_path / "src" / "androidTest" / "java" / "com" / "hazelmobile" / "cores"
    core_android_test_path.mkdir(parents=True, exist_ok=True)
    (core_android_test_path / "ExampleInstrumentedTest.kt").touch()
    
    # Create core base directories
    core_bases_path = core_java_path / "bases"
    core_bases_path.mkdir(parents=True, exist_ok=True)
    
    # Create core base subdirectories and files
    core_base_dirs = {
        "activity": ["BaseActivity.kt", "BaseActivityWithVM.kt", "LifeCycleRegister.kt"],
        "adapter": ["BaseAdapter.kt", "BaseDiffUtils.kt", "BaseViewHolder.kt", "MultipleSelectionBaseAdapter.kt", "MultipleViewBaseAdapter.kt", "Selection.kt"],
        "adapter/helpers": ["FilterManager.kt", "FilterStrategy.kt"],
        "bottomsheet": ["BaseBottomSheetDialogFragment.kt"],
        "dialog": ["BaseDialogFragment.kt"],
        "fragment": ["BaseFragment.kt", "BaseFragmentWithVM.kt"],
        "usecase": ["BaseUseCase.kt"],
        "viewmodel": ["BaseViewModel.kt"]
    }
    
    for subdir, files in core_base_dirs.items():
        (core_bases_path / Path(subdir)).mkdir(parents=True, exist_ok=True)
        for file_name in files:
            (core_bases_path / Path(subdir) / file_name).touch()
    
    # Create core extensions directory and files
    core_extensions_path = core_java_path / "extensions"
    core_extensions_path.mkdir(parents=True, exist_ok=True)
    extensions_files = ["ContextExtensions.kt", "CoreExtensions.kt", "DataTypeExtensions.kt", "ViewExtensions.kt"]
    for file_name in extensions_files:
        (core_extensions_path / file_name).touch()
    
    # Create core utils directory and files
    core_utils_path = core_java_path / "utils"
    core_utils_path.mkdir(parents=True, exist_ok=True)
    utils_files = ["Constants.kt", "LocaleHelper.kt", "Resource.kt"]
    for file_name in utils_files:
        (core_utils_path / file_name).touch()
    
    # Create build.gradle files with more realistic content using Groovy DSL syntax
    app_build_gradle_content = """
plugins {
    id 'com.android.application'
    id 'kotlin-android'
    id 'kotlin-kapt'
    id 'dagger.hilt.android.plugin'
}

android {
    compileSdk 33
    
    defaultConfig {
        applicationId "com.hazelmobile.cleanarchitecture"
        minSdk 24
        targetSdk 33
        versionCode 1
        versionName "1.0"
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = '1.8'
    }
    
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation project(':core')
    
    // Android Core
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    
    // Architecture Components
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.6.1'
    implementation 'androidx.navigation:navigation-fragment-ktx:2.5.3'
    implementation 'androidx.navigation:navigation-ui-ktx:2.5.3'
    
    // Dependency Injection
    implementation 'com.google.dagger:hilt-android:2.44'
    kapt 'com.google.dagger:hilt-android-compiler:2.44'
    
    // Networking
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:okhttp:4.10.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.10.0'
    
    // Room
    implementation 'androidx.room:room-runtime:2.5.1'
    implementation 'androidx.room:room-ktx:2.5.1'
    kapt 'androidx.room:room-compiler:2.5.1'
    
    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    (app_path / "build.gradle").write_text(app_build_gradle_content)
    
    core_build_gradle_content = """    
plugins {
    id 'com.android.library'
    id 'kotlin-android'
    id 'kotlin-kapt'
}

android {
    compileSdk 33
    
    defaultConfig {
        minSdk 24
        targetSdk 33
        
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        consumerProguardFiles "consumer-rules.pro"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = '1.8'
    }
    
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    // Android Core
    implementation 'androidx.core:core-ktx:1.9.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    
    // Architecture Components
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.6.1'
    
    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    (core_path / "build.gradle").write_text(core_build_gradle_content)
    
    # Create settings.gradle
    settings_gradle_content = """
rootProject.name = 'CleanArchitecture'
include ':app'
include ':core'
"""
    (base_path / "settings.gradle").write_text(settings_gradle_content)
    
    # Create root build.gradle
    root_build_gradle_content = """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.3.1'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.20'
        classpath 'com.google.dagger:hilt-android-gradle-plugin:2.44'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

tasks.register('clean', Delete) {
    delete rootProject.buildDir
}
"""
    (base_path / "build.gradle").write_text(root_build_gradle_content)

def create_kotlin_flow_project_structure(project_name):
    """Create a Kotlin Flow-based project structure"""
    base_path = Path(project_name)
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Reuse the clean architecture structure as a base
    create_kotlin_project_structure(project_name)
    
    # Add flow specific components
    src_path = base_path / "app" / "src" / "main" / "java" / "com" / "hazelmobile" / "cleanarchitecture"
    
    # Create flow-specific directories
    flow_dirs = [
        src_path / "data" / "flow",
        src_path / "domain" / "flow",
        src_path / "ui" / "flow",
        src_path / "ui" / "state"
    ]
    
    for directory in flow_dirs:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create flow-specific files
    flow_files = {
        src_path / "data" / "flow" / "DataFlow.kt": """
package com.hazelmobile.cleanarchitecture.data.flow

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

/**
 * Example data flow provider
 */
interface DataFlowProvider<T> {
    fun getData(): Flow<T>
}
""",
        src_path / "domain" / "flow" / "FlowUseCase.kt": """
package com.hazelmobile.cleanarchitecture.domain.flow

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOn

/**
 * Abstract Flow-based UseCase
 */
abstract class FlowUseCase<in P, R>(private val coroutineDispatcher: CoroutineDispatcher) {
    operator fun invoke(parameters: P): Flow<R> = execute(parameters)
        .flowOn(coroutineDispatcher)

    protected abstract fun execute(parameters: P): Flow<R>
}
""",
        src_path / "ui" / "state" / "UiState.kt": """
package com.hazelmobile.cleanarchitecture.ui.state

/**
 * Generic UI state for Flow-based architecture
 */
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val exception: Throwable) : UiState<Nothing>()
}
"""
    }
    
    for file_path, content in flow_files.items():
        file_path.write_text(content, encoding="utf-8")
    
    # Update build.gradle with coroutines dependencies
    app_gradle_path = base_path / "app" / "build.gradle"
    if app_gradle_path.exists():
        current_content = app_gradle_path.read_text()
        if "kotlinx-coroutines" not in current_content:
            updated_content = current_content.replace("dependencies {", """dependencies {
    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'
""")
            app_gradle_path.write_text(updated_content)

@click.group()
def cli():
    """Create Kotlin projects with Clean Architecture or Flow-based templates"""
    pass

@cli.command()
@click.argument('project_name')
def kotlin(project_name):
    """Create a Kotlin Clean Architecture project structure"""
    click.echo(f"Creating Kotlin Clean Architecture project: {project_name}")
    try:
        create_kotlin_project_structure(project_name)
        click.echo(f"Successfully created Kotlin Clean Architecture project: {project_name}")
    except Exception as e:
        click.echo(f"Error creating Kotlin project: {str(e)}", err=True)

@cli.command()
@click.argument('project_name')
def flow(project_name):
    """Create a Kotlin Flow-based project structure"""
    click.echo(f"Creating Kotlin Flow project: {project_name}")
    try:
        create_kotlin_flow_project_structure(project_name)
        click.echo(f"Successfully created Kotlin Flow project: {project_name}")
    except Exception as e:
        click.echo(f"Error creating Kotlin Flow project: {str(e)}", err=True)

def main():
    cli()

if __name__ == '__main__':
    main()