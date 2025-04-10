package bin;

public class BinStats {
	
	BinStats(){}
	BinStats(Bin b){
		id=b.id();
		taxid=b.taxid;
		if(taxid<1) {taxid=b.labelTaxid;}
		size=b.size();
		contigs=b.numContigs();
		contam=b.contam;
		complt=b.completeness;
		badContigs=b.badContigs;
		gc=b.gc();
		depth=b.depth();
		minDepth=b.minContigDepth();
		maxDepth=b.maxContigDepth();
	}
	
	String type() {
		return type(complt, contam);
	}
	
	static String type(float complt, float contam) {
		if(contam<0.01 && complt>=0.99) {return "UHQ";}
		if(contam<0.02 && complt>=0.95) {return "VHQ";}
		if(contam<0.05 && complt>=0.90) {return "HQ";}
		if(contam<0.10 && complt>=0.50) {return "MQ";}
		if(contam<0.20 || complt<0.20) {return "VLQ";}
		return "LQ";
	}
	
	int id;
	int taxid;
	long size;
	int contigs;
	int badContigs;
	float contam;
	float complt;
	float gc;
	float depth;
	float minDepth, maxDepth;
	
}
