package bin;

import java.io.File;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.concurrent.locks.ReadWriteLock;

import fileIO.ByteFile;
import fileIO.ByteStreamWriter;
import fileIO.FileFormat;
import fileIO.ReadWrite;
import shared.LineParser1;
import shared.Parse;
import shared.Parser;
import shared.PreParser;
import shared.Shared;
import shared.Timer;
import shared.Tools;
import stream.ConcurrentReadInputStream;
import stream.Read;
import structures.IntHashMap;
import structures.IntLongHashMap;
import structures.ListNum;
import structures.LongList;
import template.Accumulator;
import template.ThreadWaiter;

/**
 * Grades bins.
 * @author Brian Bushnell
 * @date Feb 8, 2025
 *
 */
public class GradeBins implements Accumulator<GradeBins.ProcessThread> {

	public static void main(String[] args){
		//Start a timer immediately upon code entrance.
		Timer t=new Timer();
		
		//Create an instance of this class
		GradeBins x=new GradeBins(args);
		
		//Run the object
		x.process(t);
		
		//Close the print stream if it was redirected
		Shared.closeStream(x.outstream);
	}
	
	public GradeBins(String[] args){
		
		{//Preparse block for help, config files, and outstream
			PreParser pp=new PreParser(args, getClass(), false);
			args=pp.args;
			outstream=pp.outstream;
		}
		
		Parser parser=new Parser();
		for(int i=0; i<args.length; i++){
			String arg=args[i];
			String[] split=arg.split("=");
			String a=split[0].toLowerCase();
			String b=split.length>1 ? split[1] : null;
			if(b!=null && b.equalsIgnoreCase("null")){b=null;}

			if(a.equals("parse_flag_goes_here")){
				//Set a variable here
			}else if(a.equals("in")){
				Tools.getFileOrFiles(b, in, true, false, false, false);
			}else if(a.equals("size")){
				totalSize=Parse.parseKMG(b);
			}else if(a.equals("minsize")){
				minSize=Parse.parseIntKMG(b);
			}else if(a.equals("ref") || a.equals("contigs") || a.equals("assembly")){
				ref=b;
			}else if(a.equals("hist")){
				hist=b;
			}else if(a.equals("report")){
				report=b;
			}else if(a.equals("taxin")){
				taxIn=b;
			}else if(a.equals("taxout")){
				taxOut=b;
			}else if(a.equals("tax") || a.equals("size")){
				tax=b;
			}else if(a.equals("loadmt")){
				loadMT=Parse.parseBoolean(b);
			}else if(a.equalsIgnoreCase("checkm")){
				checkMFile=b;
			}else if(a.equalsIgnoreCase("eukcc")){
				eukCCFile=b;
			}else if(b==null && new File(arg).isFile()){
				in.add(arg);
			}else if(b==null && new File(arg).isDirectory()){
				Tools.getFileOrFiles(arg, in, true, false, false, false);
			}else if(parser.parse(arg, a, b)){
				//do nothing
			}else{
				assert(false) : "Unknown parameter "+args[i];
				outstream.println("Unknown parameter "+args[i]);
			}
		}
		
		{//Process parser fields
			Parser.processQuality();
			
			maxReads=parser.maxReads;
//			out1=parser.out1;
		}
	}
	
	void process(Timer t){
		
		BinObject.grading=true;
		
		if(tax!=null && taxIn==null && taxOut==null) {
			boolean taxExists=(tax==null ? false : new File(tax).canRead());
			if(taxExists && ref==null) {taxIn=tax;}
			else {taxOut=tax;}
//			assert(false) : taxExists+", "+ref+", "+taxIn;
		}
		
		if(taxIn!=null) {
			if(ref!=null) {
				System.err.println("Reading from "+taxIn+" instead of "+ref);
			}
			sizeMap=loadTaxIn(taxIn);
		}else {
			sizeMap=makeSizeMap(ref);
		}
		if(taxOut!=null) {
			writeTaxOut(taxOut, sizeMap, countMap);
		}
		checkMMap=loadCheckM(checkMFile);
		eukCCMap=loadEukCC(eukCCFile);
		ArrayList<BinStats> bins=(loadMT ? loadMT(in) : loadST(in));
		
		printResults(bins);
		
		t.stop();
		outstream.println();
		outstream.println(Tools.timeReadsBasesProcessed(t, readsProcessed, basesProcessed, 8));
	}
	
	void printResults(ArrayList<BinStats> bins) {
		for(BinStats bin : bins) {
			readsProcessed+=bin.contigs;
			basesProcessed+=bin.size;
			sizes.add(bin.size);
		}
		
		if(verbose){outstream.println("Finished.");}

		outstream.println();
		printCleanDirty(bins);
		
		outstream.println();
		printL90(sizes, totalSize);

		outstream.println();
		printScore(bins, totalSize, totalContigs, taxIDsIn, true);
		
		outstream.println();
		printBinQuality(bins, minSize, outstream);
		
		if(hist!=null) {
			ChartMaker.makeChartFromBinStats(hist, bins);
		}
		if(report!=null) {
			printClusterReport(bins, minSize, report);
		}
	}
	
	public static void printScore(ArrayList<BinStats> bins, 
			long totalSize, long totalContigs, long taxIDsIn, boolean validation) {
		long cleanContigs=0, contamContigs=0;
		long cleanSize=0, contamSize=0;
		long badContigs=0;
		double compltScore=0, contamScore=0;
		double totalScore=0, totalScore2=0;
		IntHashMap tidBins=new IntHashMap();
		int labels=0;
		for(BinStats bin : bins) {
			if(bin.taxid>0) {
				tidBins.increment(bin.taxid);
				labels++;
			}
			long contam=Math.round(bin.contam*bin.size);
			contamScore+=contam;
			compltScore+=Math.round(bin.complt*(bin.size-contam));
			double score=Math.max(0, bin.complt-5*bin.contam);
			totalScore+=score;
			totalScore2+=score*score;
			badContigs+=bin.badContigs;
			if(contam<1) {
				cleanSize+=bin.size;
				cleanContigs+=bin.contigs;
			}else {
				contamSize+=bin.size;
				contamContigs+=bin.contigs;
			}
		}

		outstream.println("Sequence Recovery:           \t"+
				String.format("%.3f", (cleanSize+contamSize)*100.0/totalSize));
		outstream.println("Contig Recovery:             \t"+
				String.format("%.3f", (cleanContigs+contamContigs)*100.0/totalContigs));
		if(taxIDsIn>0) {
			outstream.println("Bad Contigs:                 \t"+
					String.format("%.3f", badContigs*100.0/(cleanContigs+contamContigs)));
			outstream.println("Genomes Represented:         \t"+
					String.format("%.3f", (tidBins.size())*100.0/taxIDsIn));
		}
		if(validation) {
			outstream.println("Completeness Score:          \t"+
					String.format("%.3f", 100*compltScore/totalSize));
			outstream.println("Contamination Score:         \t"+
					String.format("%.4f", 100*contamScore/totalSize));
//			outstream.println("Total Score:                 \t"+
//					String.format("%.2f", totalScore));
			outstream.println("Total Score:               \t"+
					String.format("%.2f", totalScore2));
		}
	}
	
	public static void printCleanDirty(ArrayList<BinStats> bins) {
		long cleanBins=0, contamBins=0;
		long cleanContigs=0, contamContigs=0;
		long cleanSize=0, contamSize=0;
		long partialCleanSize=0, partialContamSize=0;
		long badContigs=0;
		for(BinStats bin : bins) {
			long contam=Math.round(bin.contam*bin.size);
			badContigs+=bin.badContigs;
			if(contam<1) {
				cleanBins++;
				cleanSize+=bin.size;
				cleanContigs+=bin.contigs;
			}else {
				contamBins++;
				contamSize+=bin.size;
				contamContigs+=bin.contigs;
				partialCleanSize+=(bin.size-contam);
				partialContamSize+=contam;
			}
		}
		outstream.println(QuickBin.formatString("Clean Bins", 29, cleanBins, contamBins));
		outstream.println(QuickBin.formatString("Dirty Bins", 29, contamBins, cleanBins));
		outstream.println(QuickBin.formatString("Clean Bin Bases", 29, cleanSize, contamSize));
		outstream.println(QuickBin.formatString("Dirty Bin Bases", 29, contamSize, cleanSize));
		outstream.println(QuickBin.formatString("Tainted Bases", 29, 
				partialCleanSize, cleanSize+contamSize-partialCleanSize));
		outstream.println(QuickBin.formatString("Contam Bases", 29, 
				partialContamSize, cleanSize+contamSize-partialContamSize));
		outstream.println("Bad Contigs:                 \t"+
				String.format("%.3f", badContigs*100.0/(cleanContigs+contamContigs)));
	}

	public static ArrayList<BinStats> loadST(ArrayList<String> in){
		ArrayList<BinStats> bins=new ArrayList<BinStats>(in.size());
		for(String s : in) {
			final BinStats c;
			Cluster clust=loadCluster(s);
			calcContam(s, clust);
			c=new BinStats(clust);
			bins.add(c);
		}
		return bins;
	}
	
	public ArrayList<BinStats> loadMT(ArrayList<String> in){
		//Do anything necessary prior to processing
		ArrayList<BinStats> bins=new ArrayList<BinStats>(in.size());
		
		//Determine how many threads may be used
		int threads=Shared.threads();
		if(threads>16) {threads=Tools.mid(16, threads/2, 32);}
		
		//Fill a list with ProcessThreads
		ArrayList<ProcessThread> alpt=new ArrayList<ProcessThread>(threads);
		for(int i=0; i<threads; i++){
			alpt.add(new ProcessThread(in, bins, i, threads));
		}
		
		//Start the threads and wait for them to finish
		boolean success=ThreadWaiter.startAndWait(alpt, this);
		this.success&=!success;
		
		//Do anything necessary after processing
		return bins;
	}

	static Cluster loadCluster(String fname) {
		FileFormat ffin=FileFormat.testInput(fname, FileFormat.FASTA, null, true, true);
		
		final ConcurrentReadInputStream cris;
		{
			cris=ConcurrentReadInputStream.getReadInputStream(maxReads, true, ffin, null);
			cris.start();
		}
		Cluster c=new Cluster(0);		
		{
			ListNum<Read> ln=cris.nextList();
			ArrayList<Read> reads=(ln!=null ? ln.list : null);

			//ln!=null prevents a compiler potential null access warning
			while(ln!=null && reads!=null && reads.size()>0){
				if(verbose){outstream.println("Fetched "+reads.size()+" reads.");}
				
				for(int idx=0; idx<reads.size(); idx++){
					final Read r1=reads.get(idx);
					
					//  *********  Process reads here  *********
					Contig a=new Contig(r1.name(), r1.bases, (int)r1.numericID);
					c.tetramers=new int[0];
					int tid=DataLoader.parseTaxID(a.name);
					a.taxid=a.labelTaxid=tid;
					c.add(a);
				}

				cris.returnList(ln);
				if(verbose){outstream.println("Returned a list.");}
				ln=cris.nextList();
				reads=(ln!=null ? ln.list : null);
			}
			if(ln!=null){
				cris.returnList(ln.id, ln.list==null || ln.list.isEmpty());
			}
		}
		ReadWrite.closeStream(cris);
		return c;
	}
	
	static void calcContam(String fname, Cluster c) {
		fname=new File(fname).getName();
		String core=ReadWrite.stripToCore(fname);
		CCLine dummy=new CCLine(0, 0);
		CCLine checkm=(checkMMap==null ? null : checkMMap.get(core));
		CCLine eukcc=(eukCCMap==null ? null : eukCCMap.get(core));
		assert((checkMMap==null) == (checkm==null)) : checkm;
//		assert(false) : checkm;
		if(checkm==null && eukcc==null) {
			c.calcContam(sizeMap);
			return;
		}
		if(checkm==null) {checkm=dummy;}
		if(eukcc==null) {eukcc=dummy;}
		CCLine best=(checkm.completeness>=eukcc.completeness ? checkm : eukcc);
		c.completeness=best.completeness;
		c.contam=best.contam;
	}
	
	static ArrayList<BinStats> toStats(Collection<? extends Bin> bins, int minSize) {
		ArrayList<BinStats> list=new ArrayList<BinStats>();
		for(Bin b : bins) {
			if(b.size()>=minSize) {
				BinStats bs=new BinStats(b);
				list.add(bs);
			}
		}
		return list;
	}
	
	static void printClusterReport(Collection<? extends Bin> bins, int minSize, String fname) {
		ArrayList<BinStats> list=toStats(bins, minSize);
		printClusterReport(list, minSize, fname);
	}
	
	static void printClusterReport(ArrayList<BinStats> bins, int minSize, String fname) {
		if(fname==null) {return;}
		ByteStreamWriter bsw=new ByteStreamWriter(fname, true, false, false);
		bsw.start();
		bsw.print("#Bin\tSize\tContigs\tGC\tDepth\tMinDepth\tMaxDepth\tContam\tTaxID\tType\n");
		int i=0;
		for(BinStats b : bins) {
			if(b.size>=minSize) {
				bsw.print(i).tab().print(b.size).tab().print(b.contigs).tab();
				bsw.print(b.gc, 3).tab().print(b.depth, 2).tab();
				bsw.print(b.minDepth, 2).tab().print(b.maxDepth, 2).tab();
				bsw.print(b.complt, 5).tab().print(b.contam, 5).tab();
				bsw.print(b.taxid).tab().print(b.type()).nl();
				i++;
			}
		}
		bsw.poison();
	}
	
	static void printBinQuality(Collection<? extends Bin> bins, int minSize, PrintStream outstream) {
		ArrayList<BinStats> list=toStats(bins, minSize);
		printBinQuality(list, minSize, outstream);
	}
	
	static void printBinQuality(ArrayList<BinStats> bins, int minSize, PrintStream outstream) {
		long uhq=0, uhqINC=0, uhqCON=0;
		long vhq=0, vhqINC=0, vhqCON=0;
		long hq=0, hqINC=0, hqCON=0;
		long mq=0, mqINC=0, mqCON=0;
		long lq=0, lqINC=0, lqCON=0;
		long vlq=0, vlqINC=0, vlqCON=0;

		long uhqSize=0;
		long vhqSize=0;
		long hqSize=0;
		long mqSize=0;
		long lqSize=0;
		long vlqSize=0;
		
		for(BinStats b : bins) {
			final long size=b.size;
			final float comp=b.complt, contam=b.contam;
			if(size>=minSize) {
				if(contam<=0.05f && comp>=0.9f) {
					hq++;
					hqSize+=size;
					if(comp>=0.99f && contam<=0.01f) {
						uhq++;
						uhqSize+=size;
						if(comp<1) {uhqINC++;}
						if(contam>0) {uhqCON++;}
					}else if(comp>=0.95f && contam<=0.02f) {
						vhq++;
						vhqSize+=size;
						if(comp<.99f) {vhqINC++;}
						if(contam>0.01f) {vhqCON++;}
					}else {
						if(comp<.95f) {hqINC++;}
						if(contam>0.02f) {hqCON++;}
					}
				}else if(contam<0.10f && comp>=0.5f) {
					mq++;
					mqSize+=size;
					if(comp<.90f) {mqINC++;}
					if(contam>0.05f) {mqCON++;}
				}else {
					lq++;
					lqSize+=size;
					if(contam>0.20f || comp<0.20f) {//vlq
						vlq++;
						vlqSize+=size;
						if(comp<0.2f) {vlqINC++;}
						if(contam>0.2f) {vlqCON++;}
					}else {//lq, not vlq
						if(comp<0.5f) {lqINC++;}
						if(contam>0.1f) {lqCON++;}
					}
				}
			}
		}
		//Make sets inclusive
		vhq+=uhq;
		vhqSize+=uhqSize;
		
		outstream.println("Quality\tBins\tIncomp\tContam\tBases");
		outstream.println("UHQ\t"+uhq+"\t"+uhqINC+"\t"+uhqCON+"\t"+uhqSize);
		outstream.println("VHQ\t"+vhq+"\t"+vhqINC+"\t"+vhqCON+"\t"+vhqSize);
		outstream.println("HQ\t"+hq+"\t"+hqINC+"\t"+hqCON+"\t"+hqSize);
		outstream.println("MQ\t"+mq+"\t"+mqINC+"\t"+mqCON+"\t"+mqSize);
		outstream.println("LQ\t"+lq+"\t"+lqINC+"\t"+lqCON+"\t"+lqSize);
		outstream.println("VLQ\t"+vlq+"\t"+vlqINC+"\t"+vlqCON+"\t"+vlqSize);
		String hqm=""+(hq+mq/4f);
		if(hqm.endsWith(".0")) {hqm=hqm.substring(0, hqm.length()-2);}
		outstream.println("HQ+MQ/4\t"+hqm+"\t\t\t"+(hqSize+mqSize/4));
	}
	
	static void printL90FromBins(Collection<? extends Bin> bins, long basesLoaded) {
		LongList sizes=new LongList(bins.size());
		for(Bin b : bins) {
			sizes.add(b.size());
		}
		GradeBins.printL90(sizes, basesLoaded);
	}
	
	static void printL90(Collection<BinStats> bins, long basesLoaded) {
		LongList sizes=new LongList(bins.size());
		for(BinStats b : bins) {
			sizes.add(b.size);
		}
		GradeBins.printL90(sizes, basesLoaded);
	}
	
	static void printL90(LongList list, long basesLoaded) {
		long c99=(long)(0.99f*basesLoaded);
		long c95=(long)(0.95f*basesLoaded);
		long c90=(long)(0.90f*basesLoaded);
		long c80=(long)(0.80f*basesLoaded);
		long c75=(long)(0.75f*basesLoaded);
		long c50=(long)(0.50f*basesLoaded);
		long c40=(long)(0.40f*basesLoaded);
		long c30=(long)(0.30f*basesLoaded);
		long c25=(long)(0.25f*basesLoaded);
		long c20=(long)(0.20f*basesLoaded);
		long c10=(long)(0.10f*basesLoaded);
		long c05=(long)(0.05f*basesLoaded);
		long c01=(long)(0.01f*basesLoaded);
		
		list.sort();
		list.reverse();
		long prev=0, sum2=0;
		for(int i=0; i<list.size(); i++) {
			long size=list.get(i);
			prev=sum2;
			sum2+=size;
			int num=i+1;

			if(sum2>=c01 && prev<c01) {System.err.println("L01: "+size+"\t"+"N01: "+num);}
//			if(sum2>=c05 && prev<c05) {System.err.println("L05: "+size+"\t"+"N05: "+num);}
			if(sum2>=c10 && prev<c10) {System.err.println("L10: "+size+"\t"+"N10: "+num);}
			if(sum2>=c20 && prev<c20) {System.err.println("L20: "+size+"\t"+"N20: "+num);}
//			if(sum2>=c25 && prev<c25) {System.err.println("L25: "+size+"\t"+"N25: "+num);}
//			if(sum2>=c30 && prev<c30) {System.err.println("L30: "+size+"\t"+"N30: "+num);}
//			if(sum2>=c40 && prev<c40) {System.err.println("L40: "+size+"\t"+"N40: "+num);}
			if(sum2>=c50 && prev<c50) {System.err.println("L50: "+size+"\t"+"N50: "+num);}
//			if(sum2>=c75 && prev<c75) {System.err.println("L75: "+size+"\t"+"N75: "+num);}
//			if(sum2>=c80 && prev<c80) {System.err.println("L80: "+size+"\t"+"N80: "+num);}
			if(sum2>=c90 && prev<c90) {System.err.println("L90: "+size+"\t"+"N90: "+num);}
//			if(sum2>=c95 && prev<c95) {System.err.println("L95: "+size+"\t"+"N95: "+num);}
//			if(sum2>=c99 && prev<c99) {System.err.println("L99: "+size+"\t"+"N99: "+num);}
		}
	}
	
	IntLongHashMap makeSizeMap(String fname) {
		FileFormat ffin=FileFormat.testInput(fname, FileFormat.FASTA, null, true, true);
		
		final ConcurrentReadInputStream cris;
		cris=ConcurrentReadInputStream.getReadInputStream(maxReads, true, ffin, null);
		cris.start();
		
		IntLongHashMap map=new IntLongHashMap();
		countMap=new IntHashMap();
		long sizeSum=0, contigSum=0;
		{
			ListNum<Read> ln=cris.nextList();
			ArrayList<Read> reads=(ln!=null ? ln.list : null);

			//ln!=null prevents a compiler potential null access warning
			while(ln!=null && reads!=null && reads.size()>0){
				if(verbose){outstream.println("Fetched "+reads.size()+" reads.");}
				
				for(int idx=0; idx<reads.size(); idx++){
					final Read r=reads.get(idx);
					readsProcessed++;
					basesProcessed+=r.length();
					sizeSum+=r.length();
					contigSum++;
					
					//  *********  Process reads here  *********
					int tid=DataLoader.parseTaxID(r.id);
					long ret=map.increment(tid, r.length());
					countMap.increment(tid);
					if(ret==r.length() && tid>0) {taxIDsIn++;}
				}

				cris.returnList(ln);
				if(verbose){outstream.println("Returned a list.");}
				ln=cris.nextList();
				reads=(ln!=null ? ln.list : null);
			}
			if(ln!=null){
				cris.returnList(ln.id, ln.list==null || ln.list.isEmpty());
			}
		}
		if(totalSize==0) {totalSize=sizeSum;}
		if(totalContigs==0) {totalContigs=contigSum;}
		ReadWrite.closeStream(cris);
		return map;
	}
	
	private IntLongHashMap loadTaxIn(String fname) {
		ByteFile bf=ByteFile.makeByteFile(fname, true);
		LineParser1 lp=new LineParser1('\t');
		
		IntLongHashMap map=new IntLongHashMap();
		countMap=new IntHashMap();
		long sizeSum=0, contigSum=0;
		for(ListNum<byte[]> ln=bf.nextList(); ln!=null; ln=bf.nextList()) {
			for(byte[] line : ln) {
				lp.set(line);
				if(!lp.startsWith('#')) {
					int tid=lp.parseInt(0);
					long size=lp.parseLong(1);
					int contigs=lp.parseInt(2);
					long ret=map.increment(tid, size);
					countMap.increment(tid, contigs);
					sizeSum+=size;
					contigSum+=contigs;
					if(ret==size && tid>0) {taxIDsIn++;}
				}
			}
		}
		if(totalSize==0) {totalSize=sizeSum;}
		if(totalContigs==0) {totalContigs=contigSum;}
		bf.close();
		return map;
	}
	
	private void writeTaxOut(String fname, IntLongHashMap sizeMap, IntHashMap countMap) {
		ByteStreamWriter bsw=ByteStreamWriter.makeBSW(fname, overwrite, false, false);
		bsw.print("#taxID\tSize\tContigs\n");
		int[] tids=sizeMap.toArray();
		Arrays.sort(tids);
		for(int tid : tids) {
			bsw.print(tid).tab().print(sizeMap.get(tid)).tab().println(countMap.get(tid));
		}
		bsw.poison();
	}
	
	/*--------------------------------------------------------------*/
	
	public static HashMap<String, CCLine> loadCheckM(String fname){
		if(fname==null) {return null;}
		File f=new File(fname);
		if(f.isDirectory()) {
			if(!fname.endsWith("/")) {fname=fname+"/";}
			fname=fname+"quality_report.tsv";
		}
		ArrayList<byte[]> lines=ByteFile.toLines(fname);
		HashMap<String, CCLine> map=new HashMap<String, CCLine>(lines.size());
		LineParser1 lp=new LineParser1('\t');
		for(byte[] line : lines) {
			lp.set(line);
			if(!lp.startsWith("Name\t")) {
				String name=ReadWrite.stripToCore(lp.parseString(0));
				float comp=lp.parseFloat(1)/100;
				float contam=lp.parseFloat(2)/100;
				comp=Tools.mid(0, 1, comp);
				contam=Tools.mid(0, 1, contam);
				assert(comp>=0 && comp<=1) : new String(line);
//				assert(contam>=0 && contam<=1) : new String(line);
//				long size=//unavailable
				CCLine cc=new CCLine(comp, contam);
				map.put(name, cc);
			}
		}
		return map;
	}
	
	public static HashMap<String, CCLine> loadEukCC(String fname){
		if(fname==null) {return null;}
		File f=new File(fname);
		if(f.isDirectory()) {
			if(!fname.endsWith("/")) {fname=fname+"/";}
			fname=fname+"eukcc.csv";
		}
		ArrayList<byte[]> lines=ByteFile.toLines(fname);
		HashMap<String, CCLine> map=new HashMap<String, CCLine>(lines.size());
		LineParser1 lp=new LineParser1('\t');
		for(byte[] line : lines) {
			lp.set(line);
			if(!lp.startsWith("bin\tcompleteness")) {
				String name=ReadWrite.stripToCore(lp.parseString(0));
				float comp=lp.parseFloat(1)/100;
				float contam=lp.parseFloat(2)/100;
				comp=Tools.mid(0, 1, comp);
				contam=Tools.mid(0, 1, contam);
				assert(comp>=0 && comp<=1) : new String(line);
//				assert(contam>=0 && contam<=1) : new String(line);
//				long size=//unavailable
				CCLine cc=new CCLine(comp, contam);
				map.put(name, cc);
			}
		}
		return map;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------          Accumulator         ----------------*/
	/*--------------------------------------------------------------*/
	
	@Override
	public void accumulate(ProcessThread t) {
		success=(success && t.success);
	}

	@Override
	public ReadWriteLock rwlock() {
		return null;
	}

	@Override
	public boolean success() {
		return success;
	}
	
	/*--------------------------------------------------------------*/
	/*----------------         Inner Classes        ----------------*/
	/*--------------------------------------------------------------*/
	
	/** This class is static to prevent accidental writing to shared variables.
	 * It is safe to remove the static modifier. */
	static class ProcessThread extends Thread {
		
		ProcessThread(ArrayList<String> fnames_, ArrayList<BinStats> bins_, 
				int tid_, int threads_){
			fnames=fnames_;
			bins=bins_;
			tid=tid_;
			threads=threads_;
		}
		
		@Override
		public void run() {
			for(int i=tid; i<fnames.size(); i+=threads) {
				String fname=fnames.get(i);
				Cluster clust=loadCluster(fname);
				calcContam(fname, clust);
				BinStats bs=new BinStats(clust);
				synchronized(bins) {
					bins.add(bs);
				}
			}
			success=true;
		}
		
		private final ArrayList<String> fnames;
		private final ArrayList<BinStats> bins;
		private final int tid;
		private final int threads;
		boolean success=false;
		
	}
	
	/*--------------------------------------------------------------*/
	
	private static class CCLine {
		
		CCLine(float completeness_, float contam_) {
			this(completeness_, contam_, -1);
		}
		
		CCLine(float completeness_, float contam_, long size_) {
			completeness=completeness_;
			contam=contam_;
			size=size_;
			assert(completeness>=0 && completeness<=1) : completeness;
			assert(contam>=0 && contam<=1) : contam;
			assert(size>0 || size==-1);
		}
		
		public String toString() {return size+", "+completeness+", "+contam;}
		
		long size=-1;
		float completeness=-1;
		float contam=-1;
		
	}
	
	/*--------------------------------------------------------------*/
	
	private ArrayList<String> in=new ArrayList<String>();
	private String taxIn=null;
	private String taxOut=null;
	private String tax=null;
	private String ref=null;
	private String hist=null;
	private String checkMFile=null;
	private String eukCCFile=null;
	private String report=null;
	private LongList sizes=new LongList();
	private ArrayList<BinStats> bins=new ArrayList<BinStats>();
	private double contamScore=0;
	private double compltScore=0;
	private int minSize=1;
	private boolean loadMT=true;

	private	static IntLongHashMap sizeMap;
	private	static IntHashMap countMap;
	private static HashMap<String, CCLine> checkMMap;
	private static HashMap<String, CCLine> eukCCMap;
	
	/*--------------------------------------------------------------*/

	private static long maxReads=-1;
	private long readsProcessed=0, basesProcessed=0;
	private long totalSize=0, totalContigs=0;
	private long taxIDsIn=0;
	boolean overwrite=true;
	boolean success=true;
	
	/*--------------------------------------------------------------*/
	
	private static java.io.PrintStream outstream=System.err;
	public static boolean verbose=false;
	
}
