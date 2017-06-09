import numpy as np,time, scipy.io, h5py, os, psutil, resource, pdb, subprocess
from memory_profiler import profile
from threading import Thread
#intitialize variables
#create year ranges and totals
year = np.arange(1997,2012)
#create regions and sectors ranges
#number of years
nt = 17
#number of regions
nr = 49
#number of aggregations
nragg = 6

#number of sectors
ns = 200
#number of aggregations
nsagg = 76
#total matrix dimensions
nrtot = nr + nragg


nstot = ns + nsagg

#number of final demand categories
nf = 1
#households
nh = 7

@profile
def finished():
#start merging importing regions to one file called <year>_combined.hdf5
    ssst0 = time.time()
    year = np.arange(1997,2012)
    #lqw
    path = "/home/sidney/finaldata/"
    for i, x in enumerate(year):
        for j in range(55):
            #yearStr = ' '.join(map(str,year))
            #print(i)
            #print(j)
            j_offset = j + 1
            print(x)
            print(j_offset)
            subprocess.call(['h5copy', '-i', path+str(x)+"_region"+str(j_offset)+"_Footprint.hdf5",'-s', '/Footprint', '-o', str(x)+'_combined.hdf5', '-d', '/region'+str(j_offset)])

            #subprocess.call(['h5copy', '-i', '{0}','-s', '/Footprint', '-o', '{1}_combined.hdf5', '-d', '/region{2}'.format(path+str(x$

            print("Success in combining files")
                #pdb.set_trace()
                #del(bDiagVector)
                #del(yDiagVector)

            #f.close()
        #remove the region filed, as at this point there is a combined file of them
        #crop = 'rm -rf '+ path+str(x)+'_region*'
        #print(crop)
        #subprocess.call(str(crop), shell=True)

    ssst1 = time.time()
    ssstotal = ssst1-ssst0
    print("\ntotal time of merging files: "+str(ssstotal))
    #f.flush()

    #f.close()
    #log.close()


    print("finished")


def mult_diag(d, mtx, left=True):
    """Multiply a full matrix by a diagonal matrix.
    This function should always be faster than dot.

    Input:
      d -- 1D (N,) array (contains the diagonal elements)
      mtx -- 2D (N,N) array

    Output:
      mult_diag(d, mts, left=True) == dot(diag(d), mtx)
      mult_diag(d, mts, left=False) == dot(mtx, diag(d))
    """
    if left:
        return (d*mtx.T).T
    else:
        return d*mtx


#create hdf file
#create a new file and this object serves a the first starting point


    #group = f.create_group('a_group')
#f = h5py.File("/home/chai/data/built_exio.hdf5", "w")
@profile
def populate():


    #set path
    path = "/home/sidney/finaldata/"

    log = open(path+'finalBuilt_log.txt', 'w')

   
    #SOME LOGGING
    print("*** Starting script ***")
    log.write("*** Starting script ***\n")
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000
    print( "start of script the usage is (in MB):",mem)
    log.write("start of script the usage is (in MB):%s" % str(mem))
    


    #!!run loop for years #!!
    sst0 = time.time()
    for i, x in enumerate(year):

    #read stuff from matlab binary
        print("*** Loading file of year: "+ str(x)+ " ***")
        log.write("\n*** Loading file of year: "+ str(x)+ " ***\n")
        t0 = time.time()
        #IF MAT EXISTS lqw
        #mat = scipy.io.loadmat('/home/chai/data/sys_leo_%s.mat' % x) #%insert i in name
        mat = scipy.io.loadmat('/data/exiovisuals/sys_leo_%s.mat' % x) #%insert i in name
        #import aggregation matrices
        countryAgg = np.loadtxt('/home/sidney/countryAgg.dat')
        productAgg =  np.loadtxt('/home/sidney/productAgg.dat')
      
        print("*** Retrieving arrays y,b,h,leo ***", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000)
        log.write("*** Retrieving arrays y,b,h,leo ***\n")
 

        #CHECK IF THESE OBJECTS EXISTS AND THEN CHECK THE DIMENSIONS OF THEM
        y = mat['io']['y'][0][0];
        leo = mat['io']['leo'][0][0];
        b = mat['io']['b'][0][0];
        h = mat['io']['h'][0][0];

    #THIS IS A FIX BECAUSE EMISSIONS FROM HOUSEHOLDS
    #ITERATE OVER FINAL DEMAND CATEGORIES!!!!
        h = np.reshape(h, (nr, nh))[:,0]
        h = h.reshape(1,nr)

        #SOME LOGGING
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000
        print( "after retrieval of arrays the usage is (MB):",mem)
        log.write("after retrieval of arrays the usage is (MB):%s \n" % str(mem))
        t1 = time.time()
        total = t1-t0
        print("Loading time taken: "+str(total))
        log.write("Loading time taken: "+str(total)+ "\n")
        t0 = time.time()
    #populating the final demand emissions database
        print("*** Populating final demand emissions db of year: "+ str(x)+ " ***")
        log.write("*** Populating final demand emissions db of year: "+ str(x)+ " ***\n")
       
        #!! populate final demand #!!
        f = h5py.File(path+'%s_finalDemand.hdf5' % x ,'w')
        finalDemand_dset = f.create_dataset('Final_demand', (nt,nr),dtype='f')
        #try to fill in the final demand dataset with at coordinate i the array
        finalDemand_dset[i,:] = h


        t1 = time.time()
        total = t1-t0
        print("Final demand population time taken: "+str(total))
        log.write("Final demand population time taken: "+str(total)+"\n")  
        print("*** Populating footprint db of year: "+ str(x)+ " ***")
        log.write("*** Populating footprint db of year: "+ str(x)+ " ***\n")
        t0 = time.time()    

#iterating over import region "j" #nested make calculations by country of demand
        for j in range(49):


            #name footprint file year_global_id_footprint.hdf5

            #once that is finished sum the content of these files if their parent_id matches and call that file
            #year_parent_id_footprint.hdf5


            mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000
            print( "before calculating the usage is (MB):",mem)
            log.write("before calculating the usage is (MB):%s \n" % str(mem))
            #!!! first dim
            #original foot matrix
            foot = mult_diag(y[:,j],leo, left=False)
            foot = mult_diag(b[0],foot, left=True)

#Original location of removing small values
#            vpercent = 99.9
#            vtot = sum(sum(abs(foot)))
#            vmax = np.max(foot)
#            #RELATIVE truncation
#            for k in range(50):
#                foot_tmp1 = foot * (foot > (vmax * 10 ** (-1 * k)))
#                vtmp = sum(sum(abs(foot_tmp1)))
#                if (vtmp/vtot*100 > vpercent):
#                    ktmp = k
#                    break
#            foot = foot_tmp1



            foot_tmp = np.reshape(foot,[nr,ns,nr,ns])
            foot = foot_tmp
            foot_tmp = np.reshape(foot, [nr, ns * nr * ns])
            foot_tmp2 = np.dot(countryAgg, foot_tmp)

            foot_tmp3 = np.concatenate((foot_tmp2, foot_tmp))
            #pdb.set_trace()
            foot = np.reshape(foot_tmp3, [nrtot, ns, nr, ns])
            #print(foot.shape)
            #pdb.set_trace()

            #!!! second dim
            #this should be the dimensions: (ns, nrtot, nr, ns)
            ##swap first and second dim
            foot_tmp = np.transpose(foot,(1, 0, 2, 3))
            #swapped dimensions ##reshape tensor to matrix
            foot_tmp1 = np.reshape(foot_tmp, [ns, nrtot * nr * ns])
            #multiply by product aggregation
            foot_tmp2 = np.dot(productAgg, foot_tmp1)
            #concatenate aggregate and disaggregate parts
            foot_tmp3 = np.concatenate((foot_tmp2, foot_tmp1))
            ##reshape matrix to tensor
            foot_tmp4 = np.reshape(foot_tmp3, [nstot, nrtot, nr, ns])
            ##swap first and second dim
            foot= np.transpose(foot_tmp4,(1, 0, 2, 3))
            
            #!!! third dim
            foot_tmp = np.transpose(foot,(2, 1, 0, 3))
            #swapped dimensions
            foot_tmp1 = np.reshape(foot_tmp, [nr, nrtot * nstot * ns])
            foot_tmp2 = np.dot(countryAgg, foot_tmp1)
            foot_tmp3 = np.concatenate((foot_tmp2, foot_tmp1))
            #foot_tmp4 = np.transpose(foot_tmp3,(2, 1, 0, 3))
            foot_tmp4 = np.reshape(foot_tmp3, [nrtot, nstot, nrtot, ns])
            foot = np.transpose(foot_tmp4, [2, 1, 0, 3])

            #!!! fourth dim
            foot_tmp = np.transpose(foot,(3, 1, 2, 0))
            #swapped dimensions
            foot_tmp1 = np.reshape(foot_tmp, [ns, nrtot * nstot * nrtot])
            foot_tmp2 = np.dot(productAgg, foot_tmp1)
            foot_tmp3 = np.concatenate((foot_tmp2, foot_tmp1))
            #foot_tmp4 = np.transpose(foot_tmp3,(3, 1, 2, 0))
            #foot = np.reshape(foot_tmp4, [nrtot, nstot, nrtot, nstot])
            foot_tmp4 = np.reshape(foot_tmp3, [nstot,nstot,nrtot,nrtot])
            foot = np.transpose(foot_tmp4,(3, 1, 2, 0))



            mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000
            print( "after calculating the usage is (MB):",mem)
            log.write("after calculating the usage is (MB):%s \n" % str(mem))
             #open Country CSV file
            data = getfile()
            #remove first entry
            data.pop(0)

            lvls = []
            locls = []
            regC_global_id = 0

            try:
                for element in data:
                    lvls.append(element[5])
            except IndexError:
                pass
            lwst = max(lvls)
            currentLocal = (j+1)
            #parse through the file on local id, but make sure it is the lowest level
            try:
                for element in data:
                    if element[5] == lwst:
                        local = element[4]
                        globals = element[2]
                        locls.append(local +'\t'+ globals)
            except IndexError:
                pass

            nestedLocals = []
            #parse through all locals and see if there is a match
            for l in locls:

                nestedLocals.append(l.split('\t'))
            for t in nestedLocals:
                if int(currentLocal) == int(t[0]):
                    #retrieve the global id
                    regC_global_id = t[1]
                    f2 = h5py.File(path+'{0}_region{1}_Footprint.hdf5'.format(x, regC_global_id) ,'w')
						#Removing small values to reduce memory usage.
            #Absolute truncation
            eps =1000
            foot = foot * (abs(foot) > (eps))
            #vtot = foot[7-1:55, 77-1:276, 7-1:55, 77-1:276]
            #vtot = (sum(sum(sum(sum(vtot)))))
            #print (vtot/foot[0,0,0,0]*100)
            #print ("output")
						#calculate total of disagg elements
						#vtot = sum of [nr-1:nrtot, ns-1:nstot, nr-1:nrtot, ns-1:nstot]	
						#print vtot/foot[0,0,0,0]*100 and memory usage 
						#repeat for eps = 1, 1e-1, 1e-2, ..., 1e-7 a
            mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  / 1000
            print( "*after truncating the usage is (MB):",mem)
            log.write("*after truncating the usage is (MB):%s \n" % str(mem))
            #!!Fill in footprint dataset #!!

            temperal = f2.create_dataset('Footprint', (nrtot, nstot, nrtot, nstot), dtype = 'f', compression="gzip", compression_opts=9 )
           
            print("Creating file...")
            print(foot.shape)
            t0 = time.time()
            temperal[:,:,:,:] = foot
            t1 = time.time()
            print(t1-t0)
            print("Completed region:", str(j))
            del(temperal)
            del(foot)

        #do multithreading but do not do al 49 threads at the same time



        #total time of calculating and putting into a file:
        sst1 = time.time()
        sstotal = sst1-sst0
        log.write("\ntotal time of calculating and putting into a file: "+str(sstotal))

        f.flush()
        log.flush()
        #log.close()
        f.close()

def getfile():
    #open the file
    #*** > give the path to the file.
    #*************************************NACE
    #OPEN NACE DATASET FOR SECTION DATA

    f=open('/home/sidney/final_countryTree_exiovisuals.csv', 'r')
    #get the content
    F=f.read()
    #split (make an array where each element is determined by an enter)
    U = F.split('\n')
    #Create empty list !!!!!!! THIS IS THE WORKING LIST OF LIST WE NEED FOR EVERYTHING !!
    data = []
    #fill the empty list with the data (this time split even further by tabs)
    for line in U:
        data.append(line.split('\t'))
    return data


def aggRegC():
    #get the list of all global id's (we know that we need nrtot minus the aggregated part
    global_ids = list(range(nragg, nrtot))
    parent_ids = list(range(0,nragg))
    agg_ids = list(range(1,nragg))
        
    #for each year
    for i, currentYear in enumerate(year):
        print(currentYear)
           
        listofFiles = []
        for id in parent_ids:
            id = id +1
            print(id)
        
            #create the empty hdf5 files
            f2 = h5py.File('/home/sidney/finaldata/{0}_region{1}_Footprint.hdf5'.format(currentYear, id) ,'w')
            temperal = f2.create_dataset('Footprint'.format(id), (nrtot, nstot, nrtot, nstot), dtype = 'f', compression="gzip", compression_opts=9 )
            listofFiles.append(f2)
            #print(temperal)
        #print(listofFiles)
        
        #create a list of global_ids and parent_ids
        global_local = []
        splitted_global_local = []
#open CSV file and check the parent id according to the global id
         #open Country CSV file
        csv = getfile()
    #remove first entry
        csv.pop(0)
        try:
            for element in csv:
                global_id = (element[2])
                parent_id = (element[3])
                global_local.append(global_id+"\t"+parent_id)
        except IndexError:
            pass
        for l in global_local:
                splitted_global_local.append(l.split('\t'))

        #for each year create an empty dataset for numpy arrays (container aggregated dataset)
        #for all global ids (dissagregated data)
        for x in global_ids:
            #create empty aggregated file
            #f2 = h5py.File('/home/chai/finaldata/finaldata/{0}_region{1}_Footprint.hdf5'.format(x, parentName) ,'w')
            globalIdoffset = x +1
            #get path and dataset pointer to files
            with h5py.File('/home/sidney/finaldata/{0}_region{1}_Footprint.hdf5'.format(currentYear, globalIdoffset),'r') as hf:
                #print('List of arrays in this file: \n', hf.keys())
                #data = hf.get('Footprint')
                data = hf['Footprint'][()]

                for element in splitted_global_local:
                    if globalIdoffset == int(element[0]):
                        #we can retrieve its parent name
                        parentName = element[1]
                        #open files and write to it
                        for p in listofFiles:
                            import re
                            fileName = re.findall(r'"([^"]*)"', str(p))

                            current_regionOfFile = (fileName[0][11])

                            with h5py.File('/home/sidney/finaldata/{0}'.format(fileName[0]),'r+') as bla:
                                if parentName == current_regionOfFile:
                                    print("working on aggregation of region:")
                                    print(current_regionOfFile)
                                    print(parentName)
                                    print("summing region with global id:")
                                    print(globalIdoffset)
                                    currentDataset = bla.get('Footprint')
                                    my_array = bla['Footprint'][()]
                                    print(sum(sum(sum(sum(my_array)))))
                                    #aggData = my_array(data)
                                    aggData = np.add(my_array, data)
                                    currentDataset[:,:,:,:] = aggData

                                    #currentDataset[:,:,:,:] = data

                        #if parentName ==
                        #append the current data to an array that has the same name
def aggRegCTotal():
   
    agg_ids = list(range(1,nragg))

    #for each year
    for i, currentYear in enumerate(year):

        
       
        #aggregate the continents now!
        for x in agg_ids:
            id_offset = x + 1
            print(id_offset)
            print(currentYear)
            print("JUST A CHECK")
            #for each id_offset containing aggregated regions we want to sum their dataset to get to the total
            #with h5py.File('/home/sidney/finaldata/{0}_region{1}_Footprint.hdf5'.format(currentYear, id_offset),'r') as aggRegions:
            aggRegions = h5py.File('/home/sidney/finaldata/{0}_region{1}_Footprint.hdf5'.format(currentYear, id_offset), "r")
                #print('List of arrays in this file: \n', hf.keys())
                #data = hf.get('Footprint')
            data = aggRegions['Footprint'][()]
                #data = hf['Footprint'][()]
            with h5py.File('/home/sidney/finaldata/{0}_region{1}_Footprint.hdf5'.format(currentYear, '1'),'r+') as aggTotal:
                    my_array = aggTotal['Footprint'][()]
                    currentDataset = aggTotal.get('Footprint')
                    #print(sum(sum(sum(sum(my_array)))))
                    #aggData = my_array(data)
                    aggData = np.add(my_array, data)
                    currentDataset[:,:,:,:] = aggData

                    print("***Creating aggregated data for total region of import***")
                    #print("Summing region:")
                    #print(id_offset)
            
        
        #create an empty dataset and file according to the parent id
        #for each n-th value of the names list:
        #append the current global id hdf5 file to the parent dataset by:
        #1: openening the current global id dataset
        #2: check the current global id matching parent
        #3: summing the current global id dataset with the parent dataset
        #outside of the loop write to the parent file




populate()
aggRegC()
aggRegCTotal()

finished()

