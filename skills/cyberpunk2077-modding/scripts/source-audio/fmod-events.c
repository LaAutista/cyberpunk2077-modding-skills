/* Offline, read-only RoN FMOD adapter. Public C API, supplied game DLLs only.
 * No FMOD code or SDK is bundled. Never starts the game or an audio device.
 */
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef void *Handle;
typedef struct { unsigned a,b; } ParamID;
typedef struct { const char *name; ParamID id; float min,max,def; int type; unsigned flags; unsigned char guid[16]; } Param;
typedef struct { int size,maxMPEG,maxADPCM,maxXMA,maxVorbis,maxAT9,maxFADPCM,maxOpus,asioChannels; char **asioList; int *asioSpeakers; float vol0virtual; unsigned decodeBuffer; unsigned short profilePort; unsigned geometryFade; float distanceFilter; int reverbInstance,dspPool,resampler; unsigned randomSeed; int convolutionThreads,spatialObjects; } Advanced;
#define FN(lib,name,args) typedef int (__cdecl *name##_t) args; name##_t name=(name##_t)GetProcAddress(lib,#name); if(!name){fprintf(stderr,"Missing %s\n",#name);return 2;}
#define OK(call) do {int r=(call);if(r){fprintf(stderr,"%s -> FMOD %d\n",#call,r);return 3;}}while(0)
static void wav(FILE *f,unsigned bytes,unsigned rate,unsigned channels,unsigned bits,unsigned format){
  unsigned n=bytes+36,fmt=16,br=rate*channels*bits/8;unsigned short tag=format==5?3:1,ch=channels,ba=channels*bits/8,bps=bits;
  fwrite("RIFF",1,4,f);fwrite(&n,4,1,f);fwrite("WAVEfmt ",1,8,f);fwrite(&fmt,4,1,f);fwrite(&tag,2,1,f);fwrite(&ch,2,1,f);fwrite(&rate,4,1,f);fwrite(&br,4,1,f);fwrite(&ba,2,1,f);fwrite(&bps,2,1,f);fwrite("data",1,4,f);fwrite(&bytes,4,1,f);
}
int main(int argc,char **argv){
 if(argc<5){fprintf(stderr,"Usage: MODE DLL_DIRECTORY BANK_OR_FSB OUTPUT [EVENT [PARAM VALUE...]]\n");return 1;}
 char path[4096];SetDllDirectoryA(argv[2]);snprintf(path,sizeof(path),"%s\\fmod.dll",argv[2]);HMODULE core=LoadLibraryA(path);if(!core){fprintf(stderr,"LoadLibrary fmod error %lu\n",GetLastError());return 2;}
 FN(core,FMOD_System_Create,(Handle*,unsigned));FN(core,FMOD_System_GetVersion,(Handle,unsigned*,unsigned*));FN(core,FMOD_System_SetOutput,(Handle,int));FN(core,FMOD_System_Init,(Handle,int,unsigned,void*));FN(core,FMOD_System_Release,(Handle));
 FN(core,FMOD_System_CreateSound,(Handle,const char*,unsigned,void*,Handle*));FN(core,FMOD_Sound_GetNumSubSounds,(Handle,int*));FN(core,FMOD_Sound_GetSubSound,(Handle,int,Handle*));FN(core,FMOD_Sound_GetName,(Handle,char*,int));FN(core,FMOD_Sound_GetFormat,(Handle,int*,int*,int*,int*));FN(core,FMOD_Sound_GetDefaults,(Handle,float*,int*));FN(core,FMOD_Sound_GetLength,(Handle,unsigned*,unsigned));FN(core,FMOD_Sound_SeekData,(Handle,unsigned));FN(core,FMOD_System_LoadPlugin,(Handle,const char*,unsigned*,unsigned));FN(core,FMOD_Sound_ReadData,(Handle,void*,unsigned,unsigned*));FN(core,FMOD_Sound_Release,(Handle));
 if(!strcmp(argv[1],"samples")){
  Handle sys,bank;OK(FMOD_System_Create(&sys,0x00020310));unsigned version;OK(FMOD_System_GetVersion(sys,&version,0));fprintf(stderr,"FMOD version %08x\n",version);OK(FMOD_System_SetOutput(sys,2));OK(FMOD_System_Init(sys,32,0,0));OK(FMOD_System_CreateSound(sys,argv[3],0x00002080,0,&bank));int count;OK(FMOD_Sound_GetNumSubSounds(bank,&count));
  FILE *index=fopen(argv[4],"w");if(!index)return 4;fprintf(index,"index\tname\tchannels\tbits\tsample_rate\tpcm_bytes\tformat\n");
  for(int i=0;i<count;i++){Handle sound;char name[1024];int type,fmt,ch,bits;unsigned bytes;float hz;OK(FMOD_Sound_GetSubSound(bank,i,&sound));OK(FMOD_Sound_GetName(sound,name,sizeof(name)));OK(FMOD_Sound_GetFormat(sound,&type,&fmt,&ch,&bits));OK(FMOD_Sound_GetDefaults(sound,&hz,0));OK(FMOD_Sound_GetLength(sound,&bytes,4));fprintf(index,"%d\t%s\t%d\t%d\t%.0f\t%u\t%d\n",i,name,ch,bits,hz,bytes,fmt);
   if(argc>5 && (strstr(name,argv[5]) || (argc>6 && strstr(name,argv[6])))){
    snprintf(path,sizeof(path),"%s.%04d.wav",argv[4],i);FILE *f=fopen(path,"wb");if(!f)return 4;wav(f,bytes,(unsigned)hz,ch,bits,fmt);OK(FMOD_Sound_SeekData(sound,0));unsigned total=0;char buffer[65536];while(total<bytes){unsigned got=0,want=bytes-total;if(want>sizeof(buffer))want=sizeof(buffer);int r=FMOD_Sound_ReadData(sound,buffer,want,&got);if(!got || got>want){fprintf(stderr,"Read %d failed %d got %u\n",i,r,got);return 5;}fwrite(buffer,1,got,f);total+=got;}fclose(f);
   }
  }fclose(index);OK(FMOD_Sound_Release(bank));OK(FMOD_System_Release(sys));return 0;
 }
 snprintf(path,sizeof(path),"%s\\fmodstudio.dll",argv[2]);HMODULE studio=LoadLibraryA(path);if(!studio){fprintf(stderr,"LoadLibrary studio error %lu\n",GetLastError());return 2;}
 FN(studio,FMOD_Studio_System_Create,(Handle*,unsigned));FN(studio,FMOD_Studio_System_GetCoreSystem,(Handle,Handle*));FN(studio,FMOD_Studio_System_Initialize,(Handle,int,unsigned,unsigned,void*));FN(studio,FMOD_Studio_System_LoadBankFile,(Handle,const char*,unsigned,Handle*));FN(studio,FMOD_Studio_Bank_GetEventCount,(Handle,int*));FN(studio,FMOD_Studio_Bank_GetEventList,(Handle,Handle*,int,int*));FN(studio,FMOD_Studio_EventDescription_GetPath,(Handle,char*,int,int*));FN(studio,FMOD_Studio_EventDescription_GetParameterDescriptionCount,(Handle,int*));FN(studio,FMOD_Studio_EventDescription_GetParameterDescriptionByIndex,(Handle,int,Param*));FN(studio,FMOD_Studio_EventDescription_GetLength,(Handle,int*));FN(studio,FMOD_Studio_System_Release,(Handle));
 int render=!strcmp(argv[1],"render");
 FN(core,FMOD_System_SetSoftwareFormat,(Handle,int,int,int));FN(core,FMOD_System_SetDSPBufferSize,(Handle,unsigned,int));
 FN(core,FMOD_System_SetAdvancedSettings,(Handle,Advanced*));
 Handle sys=0,low=0,banks[3];OK(FMOD_Studio_System_Create(&sys,0x00020310));OK(FMOD_Studio_System_GetCoreSystem(sys,&low));unsigned version;OK(FMOD_System_GetVersion(low,&version,0));fprintf(stderr,"FMOD version %08x\n",version);Advanced advanced={0};advanced.size=sizeof(advanced);advanced.randomSeed=getenv("RON_FMOD_SEED")?(unsigned)strtoul(getenv("RON_FMOD_SEED"),0,10):1;OK(FMOD_System_SetAdvancedSettings(low,&advanced));fprintf(stderr,"RandomSeed %u\n",advanced.randomSeed);OK(FMOD_System_SetOutput(low,render?5:2));OK(FMOD_System_SetSoftwareFormat(low,48000,3,0));OK(FMOD_System_SetDSPBufferSize(low,128,4));unsigned plugin;snprintf(path,sizeof(path),"%s\\resonanceaudio.dll",argv[2]);OK(FMOD_System_LoadPlugin(low,path,&plugin,0));OK(FMOD_Studio_System_Initialize(sys,512,4,render?3:0,render?argv[4]:0));
 const char *names[]={"Master.bank","Master.strings.bank","Weapons.bank"};for(int i=0;i<3;i++){snprintf(path,sizeof(path),"%s\\%s",argv[3],names[i]);OK(FMOD_Studio_System_LoadBankFile(sys,path,0,&banks[i]));}
 if(render){
  if(argc<6 || (argc-6)%2)return 1;
  FN(studio,FMOD_Studio_System_GetEvent,(Handle,const char*,Handle*));FN(studio,FMOD_Studio_EventDescription_LoadSampleData,(Handle));FN(studio,FMOD_Studio_System_FlushSampleLoading,(Handle));FN(studio,FMOD_Studio_EventDescription_CreateInstance,(Handle,Handle*));FN(studio,FMOD_Studio_EventInstance_SetParameterByName,(Handle,const char*,float,int));FN(studio,FMOD_Studio_EventInstance_Start,(Handle));FN(studio,FMOD_Studio_System_Update,(Handle));FN(studio,FMOD_Studio_EventInstance_Release,(Handle));
  Handle desc,inst;OK(FMOD_Studio_System_GetEvent(sys,argv[5],&desc));OK(FMOD_Studio_EventDescription_LoadSampleData(desc));OK(FMOD_Studio_System_FlushSampleLoading(sys));OK(FMOD_Studio_EventDescription_CreateInstance(desc,&inst));
  for(int i=6;i<argc;i+=2)OK(FMOD_Studio_EventInstance_SetParameterByName(inst,argv[i],strtof(argv[i+1],0),1));
  FN(core,FMOD_System_GetMasterChannelGroup,(Handle,Handle*));FN(core,FMOD_ChannelGroup_SetVolume,(Handle,float));FN(core,FMOD_ChannelGroup_GetDSPClock,(Handle,unsigned long long*,unsigned long long*));Handle master;unsigned long long clock;OK(FMOD_System_GetMasterChannelGroup(low,&master));OK(FMOD_ChannelGroup_SetVolume(master,0.25f));fprintf(stderr,"MasterOutputGain 0.25\n");OK(FMOD_ChannelGroup_GetDSPClock(master,&clock,0));fprintf(stderr,"StartDSPClock %llu\n",clock);OK(FMOD_Studio_EventInstance_Start(inst));
  /* Six seconds retains firing tails; buffers are later trimmed only at silence. */
  for(int i=0;i<2251;i++)OK(FMOD_Studio_System_Update(sys));
  OK(FMOD_Studio_EventInstance_Release(inst));OK(FMOD_Studio_System_Release(sys));return 0;
 }
 int count,total;OK(FMOD_Studio_Bank_GetEventCount(banks[2],&count));Handle *events=calloc(count,sizeof(Handle));OK(FMOD_Studio_Bank_GetEventList(banks[2],events,count,&total));FILE *index=fopen(argv[4],"w");if(!index)return 4;
 for(int i=0;i<total;i++){int len,params;OK(FMOD_Studio_EventDescription_GetPath(events[i],path,sizeof(path),0));if(argc>5&&!strstr(path,argv[5]))continue;OK(FMOD_Studio_EventDescription_GetLength(events[i],&len));OK(FMOD_Studio_EventDescription_GetParameterDescriptionCount(events[i],&params));fprintf(index,"EVENT\t%s\t%d\t%d\n",path,len,params);for(int j=0;j<params;j++){Param p;memset(&p,0,sizeof(p));OK(FMOD_Studio_EventDescription_GetParameterDescriptionByIndex(events[i],j,&p));fprintf(index,"PARAM\t%s\t%.9g\t%.9g\t%.9g\t%d\t%u\n",p.name,p.min,p.max,p.def,p.type,p.flags);}}
 fclose(index);free(events);OK(FMOD_Studio_System_Release(sys));return 0;
}
